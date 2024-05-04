"""Testing module for endpoint methods /drift."""

# pylint: disable=redefined-outer-name
from pytest import mark


@mark.parametrize("concept_drift", [{"threshold": 0.5}, None], indirect=True)
@mark.parametrize("data_drift", [{"threshold": 0.5}, None], indirect=True)
def test_running_drift(monitor, drift_info):
    """Test the a new drift has sent to server and the state is running."""
    assert drift_info["model_id"] == monitor.model_id
    assert drift_info["status"] == "Running"
