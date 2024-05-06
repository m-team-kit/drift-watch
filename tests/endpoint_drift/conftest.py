"""Testing module for endpoint methods /drift."""

# pylint: disable=redefined-outer-name
from pytest import fixture


@fixture(scope="module")
def path(request):
    """Return the path for the request."""
    if not hasattr(request, "param"):
        return "/api/drift"
    if request.param is None:
        return None
    return request.param
