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
        """Test the 403 response."""
        assert response.status_code == 403


@mark.parametrize("auth", ["invalid_token"], indirect=True)
@mark.usefixtures("accept_authorization")
class TestNotRegistered(CommonTests):
    """Test the bad_key parameter."""

    def test_error_msg(self, response):
        """Test message contains useful information."""
        assert response.json["error"] == "Forbidden"
        description = response.json["error_description"]
        assert description == "User user_1@issuer_1 does not meet requirements"
        details = response.json["error_details"]
        assert details == "Evaluation of: is_registered"
