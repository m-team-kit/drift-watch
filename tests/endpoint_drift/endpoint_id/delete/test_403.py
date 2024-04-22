"""Testing module for endpoint methods /drift."""

# pylint: disable=redefined-outer-name
from pytest import mark


class CommonTests:
    """Common tests for the /drift endpoint."""

    def test_status_code(self, response):
        """Test the 403 response."""
        assert response.status_code == 403


@mark.parametrize(
    "drift_id",  # Parametrize by class to cluster tests in same group
    [  # List of drift ids to test in this class
        "00000000-0000-0001-0001-000000000001",
    ],
    indirect=True,
)
class DriftV100(CommonTests):
    """Tests for V100 drift ids."""


@mark.parametrize("auth", ["invalid_token"], indirect=True)
@mark.usefixtures("accept_authorization")
class TestNotRegistered(DriftV100):
    """Test response when user is not registered."""

    def test_error_msg(self, response):
        """Test message contains useful information."""
        assert response.json["error"] == "Forbidden"
        description = response.json["error_description"]
        assert description == "User user_1@issuer_1 does not meet requirements"


@mark.parametrize("auth", ["mock-token"], indirect=True)
@mark.parametrize(
    "drift_id",  # Parametrize by class to cluster tests in same group
    [  # List of drift ids to test in this class
        "00000000-0000-0001-0001-000000000002",
        "4401dde0-32f2-4db3-8154-6cd88764f699",
    ],
    indirect=True,
)
@mark.parametrize("with_database", ["database_1"], indirect=True)
@mark.usefixtures("with_context", "with_database")
@mark.usefixtures("accept_authorization")
class TestNotOwned(CommonTests):
    """Test response when drift does not belong to owner."""

    def test_error_msg(self, response):
        """Test message contains useful information."""
        assert response.json["error"] == "Forbidden"
        description = response.json["error_description"]
        assert description == "User user_1@issuer_1 does not meet requirements"
