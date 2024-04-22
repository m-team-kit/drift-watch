"""Testing module for endpoint methods /drift."""

# pylint: disable=redefined-outer-name
from pytest import fixture


@fixture(scope="module")
def path(request):
    """Return the path for the request."""
    return request.param if hasattr(request, "param") else "/drift"


@fixture(scope="module")
def collection(database):
    """Return a collection connection to the database."""
    return database["app.blueprints.drift"]


@fixture(scope="class")
def db_item(response, collection):
    """Return the item from the database."""
    item = collection.find_one({"_id": response.json["id"]})
    if item is not None:
        item["id"] = item.pop("_id")
    return item
