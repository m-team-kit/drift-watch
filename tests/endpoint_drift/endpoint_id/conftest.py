"""Testing module for endpoint methods /drift."""

# pylint: disable=redefined-outer-name
from pytest import fixture


@fixture(scope="class")
def path(request, drift_id):
    """Return the path for the request."""
    if hasattr(request, "param") and request.param:
        return request.param
    return f"/drift/{drift_id}"


@fixture(scope="class")
def db_item(response, collection, drift_id):
    """Return the item from the database."""
    item = collection.find_one({"_id": str(drift_id)})
    if item is not None:
        item["id"] = item.pop("_id")
    return item


@fixture(scope="class")
def drift_id(request):
    """Return Drift id from request param."""
    return request.param
