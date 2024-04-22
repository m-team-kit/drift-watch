"""Testing module for endpoint methods /drift."""

# pylint: disable=redefined-outer-name
from datetime import datetime as dt
from datetime import timezone as tz

from pytest import fixture


@fixture(scope="class", name="response")
def request(client, path, request_kwds):
    """Create a request object."""
    yield client.get(path, **request_kwds)


@fixture(scope="class")
def body(request, schema_version, datetime, model_info, drifts):
    """Inject and return a request body."""
    kwds = {}  # Update the body with the test parameters
    for key, value in [
        ("schema_version", schema_version),
        ("datetime", datetime),
        ("job_status", model_info["job_status"]),
        ("model", model_info["model"]),
        ("concept_drift", drifts["concept_drift"]),
        ("data_drift", drifts["data_drift"]),
    ]:
        kwds.update({key: value} if value else {})
    kwds.update(request.param if hasattr(request, "param") else {})
    return kwds if kwds else None


@fixture(scope="class")
def schema_version(request):
    """Inject and return a collection name."""
    return request.param


@fixture(scope="class", params=["2020-01-10", None])
def start_date(request):
    """Inject and return a start date."""
    return request.param


@fixture(scope="class")
def start_dateiso(start_date):
    """Return the start date in iso format."""
    if start_date:
        return dt.fromisoformat(start_date).replace(tzinfo=tz.utc)
    return None


@fixture(scope="class", params=["2020-01-20", None])
def end_date(request):
    """Inject and return an end date."""
    return request.param


@fixture(scope="class")
def end_dateiso(end_date):
    """Return the end date in iso format."""
    if end_date:
        return dt.fromisoformat(end_date).replace(tzinfo=tz.utc)
    return None


@fixture(scope="class")
def datetime(request, start_date, end_date):
    """Return a datetime filter."""
    datetime = request.param if hasattr(request, "param") else {}
    datetime.update({"$gte": start_date} if start_date else {})
    datetime.update({"$lte": end_date} if end_date else {})
    return datetime


@fixture(scope="class", params=["Running", "Completed", "Failed", None])
def job_status(request):
    """Inject and return a job status."""
    return request.param


@fixture(scope="class", params=["model_1", None])
def model(request):
    """Inject and return a drift detection type."""
    return request.param


@fixture(scope="class")
def model_info(model, job_status):
    """Return the model info from the parameters as dict."""
    return {"model": model, "job_status": job_status}


@fixture(scope="class")
def concept_drift(request):
    """Inject and return a concept drift detection type."""
    return request.param if hasattr(request, "param") else None


@fixture(scope="class")
def data_drift(request):
    """Inject and return a data drift detection type."""
    return request.param if hasattr(request, "param") else None


@fixture(scope="class")
def drifts(concept_drift, data_drift):
    """Return the drifts from the parameters as dict."""
    return {"concept_drift": concept_drift, "data_drift": data_drift}
