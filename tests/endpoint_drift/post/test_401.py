"""Testing module for endpoint methods /drift."""

# pylint: disable=redefined-outer-name
from pytest import mark


@mark.parametrize("job_status", ["Running"], indirect=True)
@mark.parametrize("model", ["example_1"], indirect=True)
@mark.parametrize("concept_drift", [None], indirect=True)
@mark.parametrize("data_drift", [None], indirect=True)
class CommonTests:
    """Common tests for the /drift endpoint."""

    def test_status_code(self, response):
        """Test the 401 response."""
        assert response.status_code == 401


@mark.parametrize("auth", [None], indirect=True)
class TestMissingToken(CommonTests):
    """Test when missing bearer token parameter."""

    def test_error_msg(self, response):
        """Test message contains useful information."""
        assert response.json["error"] == "Unauthenticated"
        description = response.json["error_description"]
        assert description == "No authorization header"


@mark.parametrize("auth", ["invalid_token"], indirect=True)
class TestInvalidToken(CommonTests):
    """Test the bad_key parameter."""

    def test_error_msg(self, response):
        """Test message contains useful information."""
        assert response.json["error"] == "Unauthenticated"
        description = response.json["error_description"]
        assert description == "User identity could not be determined"
