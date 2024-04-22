"""Testing module for endpoint methods /drift."""

# pylint: disable=redefined-outer-name
from pytest import fixture


@fixture(scope="class", name="response")
def request(client, path, request_kwds):
    """Create a request object."""
    yield client.put(path, **request_kwds)


@fixture(scope="class")
def body(request, model, job_status, drifts):
    """Inject and return a request body."""
    kwds = {}  # Update the body with the test parameters
    for key, value in [
        ("model", model),
        ("job_status", job_status),
        ("concept_drift", drifts["concept_drift"]),
        ("data_drift", drifts["data_drift"]),
    ]:
        kwds.update({key: value} if value else {})
    kwds.update(request.param if hasattr(request, "param") else {})
    return kwds if kwds else None


@fixture(scope="class", params=["ex_model"])
def model(request):
    """Return an end date."""
    return request.param


@fixture(scope="class", params=["Running", "Completed", "Failed"])
def job_status(request):
    """Return a job status for the drift."""
    return request.param


@fixture(
    scope="class",
    params=[
        {"drift": True, "parameters": {"p_value": 0.1}},
        {"drift": False, "parameters": {"p_value": 0.1}},
        None,
    ],
)
def concept_drift(request):
    """Return a concept drift detection."""
    return request.param


@fixture(
    scope="class",
    params=[
        {"drift": True, "parameters": {"p_value": 0.1}},
        {"drift": False, "parameters": {"p_value": 0.1}},
        None,
    ],
)
def data_drift(request):
    """Return a data drift detection."""
    return request.param


@fixture(scope="class")
def drifts(concept_drift, data_drift):
    """Return the drifts from the parameters as dict."""
    return {"concept_drift": concept_drift, "data_drift": data_drift}
