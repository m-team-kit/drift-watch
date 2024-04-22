"""Testing module for endpoint methods /drift."""

# pylint: disable=redefined-outer-name
from pytest import mark


@mark.parametrize("auth", ["mock-token"], indirect=True)
@mark.parametrize("job_status", ["Running"], indirect=True)
@mark.parametrize("model", ["example_1"], indirect=True)
@mark.parametrize("with_database", ["database_1"], indirect=True)
@mark.usefixtures("with_context", "with_database")
@mark.usefixtures("accept_authorization")
class CommonTests:
    """Common tests for the /drift endpoint."""

    def test_status_code(self, response):
        """Test the 422 response."""
        assert response.status_code == 422


@mark.parametrize(
    "drift_id",  # Parametrize by class to cluster tests in same group
    [  # List of drift ids to test in this class
        "00000000-0000-0001-0001-000000000001",
    ],
    indirect=True,
)
class DriftV100(CommonTests):
    """Tests for V100 drift ids."""


@mark.parametrize("body", [{"bad_key": "val"}], indirect=True)
class TestBadBodyKey(DriftV100):
    """Test the bad_key parameter."""

    def test_error_msg(self, response):
        """Test message contains useful information."""
        assert "bad_key" in response.json["errors"]["json"]
        error = response.json["errors"]["json"]["bad_key"]
        assert error == ["Unknown field."]


@mark.parametrize(
    argnames="concept_drift",
    argvalues=[
        {"drift": True},  # Raise error for missing "parameters" key
        {"drift": True, "parameters": {}},  # """ empty "parameters" key
    ],
    indirect=True,
)
class TestMissingCParam(DriftV100):

    def test_error_msg(self, response):
        """Test message contains useful information."""
        assert "concept_drift" in response.json["errors"]["json"]
        error = response.json["errors"]["json"]["concept_drift"]
        assert error == {"_schema": ["Include parameters if drift."]}


@mark.parametrize(
    argnames="concept_drift",
    argvalues=[
        {"drift": "non-bool"},  # Raise error for non-boolean value
        {"drift": "non-bool", "parameters": {"p_value": 5}},  # Idem
    ],
    indirect=True,
)
class TestNoCBoolDrift(DriftV100):

    def test_error_msg(self, response):
        """Test message contains useful information."""
        assert "concept_drift" in response.json["errors"]["json"]
        error = response.json["errors"]["json"]["concept_drift"]
        assert error == {"drift": ["Not a valid boolean."]}


@mark.parametrize(
    argnames="concept_drift",
    argvalues=[
        {"parameters": {}},  # Raise error for missing drift key
        {"parameters": {"p_value": 0}},  # Raise error for missing drift key
    ],
    indirect=True,
)
class TestMissingCDrift(DriftV100):

    def test_error_msg(self, response):
        """Test message contains useful information."""
        assert "concept_drift" in response.json["errors"]["json"]
        error = response.json["errors"]["json"]["concept_drift"]
        assert error == {"drift": ["Missing data for required field."]}


@mark.parametrize(
    argnames="concept_drift",
    argvalues=[
        {"drift": True, "parameters": "non-map"},  # Raise no map value
    ],
    indirect=True,
)
class TestNoMapCParam(DriftV100):

    def test_error_msg(self, response):
        """Test message contains useful information."""
        assert "concept_drift" in response.json["errors"]["json"]
        error = response.json["errors"]["json"]["concept_drift"]
        assert error == {"parameters": ["Not a valid mapping type."]}
