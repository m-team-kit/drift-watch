"""Testing module for endpoint methods /user."""

# pylint: disable=redefined-outer-name
from pytest import mark


@mark.parametrize("auth", ["mock-token"], indirect=True)
@mark.parametrize("with_database", ["database_1"], indirect=True)
@mark.usefixtures("with_context", "with_database")
@mark.usefixtures("accept_authorization")
class CommonTests:
    """Common tests for the /drift endpoint."""

    def test_status_code(self, response):
        """Test the 409 response."""
        assert response.status_code == 409


@mark.parametrize("subiss", [("user_1", "issuer_1")], indirect=True)
class TestConflict(CommonTests):
    """Test the bad_key parameter."""

    def test_error_msg(self, response):
        """Test message contains useful information."""
        assert response.json["code"] == 409
        assert response.json["status"] == "Conflict"
        assert response.json["message"] == "User already exists"
