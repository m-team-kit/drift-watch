"""Testing module for endpoint methods /drift."""

# pylint: disable=redefined-outer-name
from pytest import mark


@mark.parametrize("auth", ["mock-token"], indirect=True)
@mark.parametrize("with_database", ["database_1"], indirect=True)
@mark.usefixtures("with_context", "with_database")
@mark.usefixtures("accept_authorization")
class CommonTests:
    """Test the bad_key parameter."""

    def test_status_code(self, response):
        """Test the 404 response."""
        assert response.status_code == 404


@mark.parametrize(
    "drift_id",  # Parametrize by class to cluster tests in same group
    [  # List of drift ids to test in this class
        "4401dde0-32f2-4db3-8154-6cd88764f699",
    ],
    indirect=True,
)
class DriftV100(CommonTests):
    """Tests for V100 drift ids."""


@mark.parametrize("entitlements", [["iam:admin"]], indirect=True)
class TestNotFound(DriftV100):
    """Test the response when drift is not in the database."""

    def test_error(self, response):
        """Test message contains useful information."""
        assert response.json["code"] == 404
        assert response.json["status"] == "Not Found"
