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
def tags(request):
    """Return the tags for the monitor."""
    default_tags = ["drift_type", "method_name"]
    return request.param if hasattr(request, "param") else default_tags


@fixture(scope="function")
def monitor(experiment, tags):
    """Return a DriftMonitor instance."""
    with DriftMonitor(experiment.name, "model_1", tags) as monitor:
        yield monitor


@fixture(scope="function")
def exit_normal(monitor):
    """Closes the context for the monitor."""
    return monitor.__exit__(None, None, None)


@fixture(scope="function")
def exit_error(monitor):
    """Closes the context simulating an error."""
    return monitor.__exit__(ValueError, None, None)


@fixture(scope="function")
def drift(monitor, drift_detected, parameters):
    """Add concept drift to the monitor."""
    return monitor(drift_detected, parameters)
