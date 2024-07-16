"""Pytest configuration for testing the client."""

# pylint: disable=redefined-outer-name

from drift_monitor import DriftMonitor, register
import requests
from pytest import fixture


@fixture(scope="session", autouse=True)
def register_user():
    """Register a user in the drift monitor."""
    register(accept_terms=True)


@fixture(scope="function")
def monitor():
    """Return a DriftMonitor instance."""
    with DriftMonitor("model_1") as monitor:
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
        request.param = {"threshold": 0.5}
    if request.param is None:
        return None
    monitor.concept(True, request.param)
    return request.param


@fixture(scope="function", autouse=True)
def data_drift(request, monitor):
    """Add data drift to the monitor."""
    if not hasattr(request, "param"):
        request.param = {"threshold": 0.5}
    if request.param is None:
        return None
    monitor.data(True, request.param)
    return request.param


@fixture(scope="function")
def drift_info(endpoint, monitor):
    """Retrieves the drift information from the server."""
    url = f"https://{endpoint}/api/latest/drift/{monitor.drift['id']}"
    response = requests.get(url, timeout=5, verify=False)
    response.raise_for_status()
    return response.json()
