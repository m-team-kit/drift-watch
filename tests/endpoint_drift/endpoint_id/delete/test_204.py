"""Testing module for endpoint methods /drift."""

# pylint: disable=redefined-outer-name
from pytest import mark


@mark.parametrize("auth", ["mock-token"], indirect=True)
@mark.parametrize("with_database", ["database_1"], indirect=True)
@mark.usefixtures("with_context", "with_database")
@mark.usefixtures("accept_authorization")
class CommonTests:
    """Common tests for the /drift/<drift_id> endpoint."""

    def test_status_code(self, response):
        """Test the 204 response."""
        assert response.status_code == 204

    def test_not_in_database(self, db_item):
        """Test the response items are in the database."""
        assert db_item is None


@mark.parametrize(
    "drift_id",  # Parametrize by class to cluster tests in same group
    [  # List of drift ids to test in this class
        "00000000-0000-0001-0001-000000000001",
    ],
    indirect=True,
)
class DriftV100(CommonTests):
    """Tests for V100 drift ids."""


class TestGetIdV100(DriftV100):
    """Test the responses items."""
