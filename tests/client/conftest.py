"""Pytest configuration for testing the client."""

# pylint: disable=redefined-outer-name

import uuid

from drift_monitor import DriftMonitor, new_experiment, register
from pytest import fixture


@fixture(scope="session", autouse=True)
def register_user():
    """Register a user in the drift monitor."""
    register(accept_terms=True)


@fixture(scope="session")
def experiment():
    """Create and return an experiment."""
    experiment_name = f"experiment_{uuid.uuid4().hex}"
    description = "Some experiment description"
    return new_experiment(experiment_name, description)


@fixture(scope="function")
def monitor(experiment):
    """Return a DriftMonitor instance."""
    with DriftMonitor(experiment["name"], "model_1") as monitor:
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
