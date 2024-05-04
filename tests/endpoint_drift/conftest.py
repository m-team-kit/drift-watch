"""Testing module for endpoint methods /drift."""

# pylint: disable=redefined-outer-name
from pytest import fixture


@fixture(scope="module")
def path(endpoint):
    """Return the path for the request."""
    return f"{endpoint}/api/drift"
