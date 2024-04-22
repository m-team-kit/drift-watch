"""Testing module for endpoint methods /user."""

# pylint: disable=redefined-outer-name
from pytest import mark


@mark.parametrize("auth", ["mock-token"], indirect=True)
@mark.parametrize("created_before", [None], indirect=True)
@mark.parametrize("created_after", [None], indirect=True)
@mark.parametrize("issuer", [None], indirect=True)
class CommonTests:
    """Common tests for the /drift endpoint."""

    def test_status_code(self, response):
        """Test the 403 response."""
        assert response.status_code == 403


@mark.usefixtures("accept_authorization")
class TestNotAdmin(CommonTests):
    """Test when user is not administrator parameter."""

    def test_error_msg(self, response):
        """Test message contains useful information."""
        assert response.json["error"] == "Forbidden"
        description = response.json["error_description"]
        assert description == "User user_1@issuer_1 does not meet requirements"
        details = response.json["error_details"]
        assert details == "Evaluation of: is_admin"
