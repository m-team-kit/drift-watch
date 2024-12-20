"""Testing module for endpoint methods /drift."""

# pylint: disable=redefined-outer-name
from pytest import mark


@mark.parametrize("drift_detected", [True])
@mark.parametrize("parameters", [{"some_field": 0.1}])
@mark.usefixtures("monitor", "drift")
def test_running(db, experiment, tags):
    """Test the a new drift has sent to server and the state is running."""
    drift = db[f"app.{experiment.id}"].find_one({"job_status": "Running"})
    assert drift != []  # Drift is not empty
    assert drift["tags"] == tags  # Tags are set when opening context
    assert drift["drift_detected"] is False  # Context not closed
    assert drift["parameters"] == {}  # Context not closed


@mark.parametrize("drift_detected", [True])
@mark.parametrize("parameters", [{"some_field": 0.1}])
@mark.usefixtures("monitor", "drift", "exit_normal")
def test_completed(db, experiment, drift_detected, parameters):
    """Test the concept drift content is saved and job completed."""
    drift = db[f"app.{experiment.id}"].find_one({"job_status": "Completed"})
    assert drift["drift_detected"] == drift_detected  # Check saved
    assert drift["parameters"] == parameters  # Check saved
