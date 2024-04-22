"""Testing module for endpoint methods /user."""

# pylint: disable=redefined-outer-name
from pytest import mark


@mark.parametrize("body", [None], indirect=True)
class CommonTests:
    """Common tests for the /user endpoint."""

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
    """Test when invalid token parameter."""

    def test_error_msg(self, response):
        """Test message contains useful information."""
        assert response.json["error"] == "Unauthenticated"
        description = response.json["error_description"]
        assert description == "User identity could not be determined"
