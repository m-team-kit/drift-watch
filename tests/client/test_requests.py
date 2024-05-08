"""Testing module for endpoint methods /drift."""

# pylint: disable=redefined-outer-name
from pytest import mark


@mark.parametrize("concept_drift", [{"threshold": 0.5}, None], indirect=True)
@mark.parametrize("data_drift", [{"threshold": 0.5}, None], indirect=True)
def test_running_drift(monitor, drift_info):
    """Test the a new drift has sent to server and the state is running."""
    assert drift_info["model"] == monitor.model_id
    assert drift_info["job_status"] == "Running"


@mark.parametrize("concept_drift", [{"threshold": 0.5}], indirect=True)
@mark.usefixtures("exit_normal")
def test_concept_saved(concept_drift, drift_info):
    """Test the concept drift content is saved and job completed."""
    full_drift = {"drift": True, "parameters": concept_drift}
    assert drift_info["concept_drift"] == full_drift
    assert drift_info["job_status"] == "Completed"


@mark.parametrize("data_drift", [{"threshold": 0.5}], indirect=True)
@mark.usefixtures("exit_normal")
def test_data_saved(data_drift, drift_info):
    """Test the data drift content is saved and job completed."""
    full_drift = {"drift": True, "parameters": data_drift}
    assert drift_info["data_drift"] == full_drift
    assert drift_info["job_status"] == "Completed"
