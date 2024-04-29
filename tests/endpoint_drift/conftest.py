"""Testing module for endpoint methods /drift."""

# pylint: disable=redefined-outer-name
from pytest import fixture


@fixture(scope="module")
def path(base_url):
    """Return the path for the request."""
    return f"http://{base_url}/api/drift"
