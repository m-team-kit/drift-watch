"""Testing module for endpoint methods /user."""

# pylint: disable=redefined-outer-name
from datetime import datetime as dt
from datetime import timezone as tz

from pytest import fixture


@fixture(scope="class", name="response")
def request(client, path, request_kwds):
    """Create a request object."""
    yield client.get(path, **request_kwds)


@fixture(scope="class")
def body(request, created_at, user_info, drift_ids):
    """Inject and return a request body."""
    kwds = {}  # Update the body with the test parameters
    for key, value in [
        ("created_at", created_at),
        ("subject", user_info["subject"]),
        ("issuer", user_info["issuer"]),
        ("email", user_info["email"]),
        ("drift_ids", drift_ids),
    ]:
        kwds.update({key: value} if value else {})
    kwds.update(request.param if hasattr(request, "param") else {})
    return kwds if kwds else None


@fixture(scope="class", params=["2020-01-04", None])
def created_after(request):
    """Inject and return a creation after date."""
    return request.param


@fixture(scope="class")
def after_dateiso(created_after):
    """Return the created after date in iso format."""
    if created_after:
        return dt.fromisoformat(created_after).replace(tzinfo=tz.utc)
    return None


@fixture(scope="class", params=["2020-01-08", None])
def created_before(request):
    """Inject and return a creation before date."""
    return request.param


@fixture(scope="class")
def before_dateiso(created_before):
    """Return the created before date in iso format."""
    if created_before:
        return dt.fromisoformat(created_before).replace(tzinfo=tz.utc)
    return None


@fixture(scope="class")
def created_at(request, created_after, created_before):
    """Return a datetime filter."""
    datetime = request.param if hasattr(request, "param") else {}
    datetime.update({"$gte": created_after} if created_after else {})
    datetime.update({"$lte": created_before} if created_before else {})
    return datetime


@fixture(scope="class", params=["issuer_1", None])
def issuer(request):
    """Inject and return issuer information type."""
    return request.param


@fixture(scope="class")
def user_info(issuer):  # Add more user info if needed
    """Return the user drift ids filter."""
    return {"subject": None, "issuer": issuer, "email": None}


@fixture(scope="class", params=[None])  # TODO: add filter
def drift_ids(request):
    """Return the user drift ids filter."""
    return request.param
