"""Pytest configuration for testing the client."""

# pylint: disable=redefined-outer-name

from drift_monitor import DriftMonitor
import requests
from pytest import fixture


@fixture(scope="function")
def monitor(mytoken):
    """Return a DriftMonitor instance."""
    with DriftMonitor("model_1", mytoken) as monitor:
        yield monitor


@fixture(scope="function")
def exit_normal(monitor):
    """Closes the context for the monitor."""
    return monitor.__exit__(None, None, None)


@fixture(scope="function")
def exit_error(monitor):
    """Closes the context simulating an error."""
    return monitor.__exit__(ValueError, None, None)


@fixture(scope="function", autouse=True)
def concept_drift(request, monitor):
    """Add concept drift to the monitor."""
    if not hasattr(request, "param"):
        return monitor.concept(True, {"threshold": 0.5})
    if request.param is None:
        return None
    return monitor.concept(True, request.param)


@fixture(scope="function", autouse=True)
def data_drift(request, monitor):
    """Add data drift to the monitor."""
    if not hasattr(request, "param"):
        return monitor.data(True, {"threshold": 0.5})
    if request.param is None:
        return None
    return monitor.data(True, request.param)


@fixture(scope="function")
def drift_info(endpoint, monitor):
    """Retrieves the drift information from the server."""
    url = f"http://{endpoint}/drift/api/{monitor.drift['id']}"
    return requests.get(url, timeout=5).json()
