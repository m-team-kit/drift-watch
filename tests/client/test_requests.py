"""Testing module for endpoint methods /drift."""

# pylint: disable=redefined-outer-name
from pytest import mark


@mark.parametrize("concept_drift", [{"threshold": 0.5}, None], indirect=True)
@mark.parametrize("data_drift", [{"threshold": 0.5}, None], indirect=True)
@mark.usefixtures("monitor")
def test_running_drift(db, experiment):
    """Test the a new drift has sent to server and the state is running."""
    drift = db[f"app.{experiment['id']}"].find_one({"job_status": "Running"})
    assert drift["concept_drift"] == {"drift": False, "parameters": {}}
    assert drift["data_drift"] == {"drift": False, "parameters": {}}


@mark.parametrize("concept_drift", [{"threshold": 0.5}], indirect=True)
@mark.usefixtures("exit_normal")
def test_concept_saved(db, experiment, concept_drift):
    """Test the concept drift content is saved and job completed."""
    full_drift = {"drift": True, "parameters": concept_drift}
    drift = db[f"app.{experiment['id']}"].find_one({"job_status": "Completed"})
    assert drift["concept_drift"] == full_drift


@mark.parametrize("data_drift", [{"threshold": 0.5}], indirect=True)
@mark.usefixtures("exit_normal")
def test_data_saved(db, experiment, data_drift):
    """Test the data drift content is saved and job completed."""
    full_drift = {"drift": True, "parameters": data_drift}
    drift = db[f"app.{experiment['id']}"].find_one({"job_status": "Completed"})
    assert drift["data_drift"] == full_drift
