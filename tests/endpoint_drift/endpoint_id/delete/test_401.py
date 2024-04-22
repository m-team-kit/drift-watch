"""Testing module for endpoint methods /drift."""

# pylint: disable=redefined-outer-name
from pytest import mark


class CommonTests:
    """Common tests for the /drift endpoint."""

    def test_status_code(self, response):
        """Test the 401 response."""
        assert response.status_code == 401


@mark.parametrize(
    "drift_id",  # Parametrize by class to cluster tests in same group
    [  # List of drift ids to test in this class
        "00000000-0000-0001-0001-000000000001",
    ],
    indirect=True,
)
class DriftV100(CommonTests):
    """Tests for V100 drift ids."""


@mark.parametrize("auth", [None], indirect=True)
class TestMissingToken(DriftV100):
    """Test the bad_key parameter."""

    def test_error_msg(self, response):
        """Test message contains useful information."""
        assert response.json["error"] == "Unauthenticated"
        description = response.json["error_description"]
        assert description == "No authorization header"


@mark.parametrize("auth", ["invalid_token"], indirect=True)
class TestInvalidToken(DriftV100):
    """Test the bad_key parameter."""

    def test_error_msg(self, response):
        """Test message contains useful information."""
        assert response.json["error"] == "Unauthenticated"
        description = response.json["error_description"]
        assert description == "User identity could not be determined"
