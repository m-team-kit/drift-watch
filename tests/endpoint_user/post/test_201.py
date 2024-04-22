"""Testing module for endpoint methods /user."""

# pylint: disable=redefined-outer-name
import uuid
from datetime import datetime as dt

from pytest import mark


@mark.parametrize("auth", ["mock-token"], indirect=True)
@mark.parametrize("with_database", ["database_2"], indirect=True)
@mark.usefixtures("with_context", "with_database")
@mark.usefixtures("accept_authorization")
class CommonTests:
    """Common tests for the /drift endpoint."""

    def test_status_code(self, response):
        """Test the 201 response."""
        assert response.status_code == 201

    def test_in_database(self, response, db_item):
        """Test the response items are in the database."""
        assert db_item is not None
        assert response.json == db_item

    def test_user_id(self, response):
        """Test the response item have correct id."""
        assert uuid.UUID(response.json["id"]).version == 4

    def test_datetime(self, response):
        """Test the response item has a correct created_at."""
        assert dt.fromisoformat(response.json["created_at"])

    def test_user_subject(self, response, subiss):
        """Test the response item have correct subject."""
        assert response.json["subject"] == subiss[0]

    def test_user_issuer(self, response, subiss):
        """Test the response item have correct issuer."""
        assert response.json["issuer"] == subiss[1]


@mark.parametrize("subiss", [("user_1", "issuer_1")], indirect=True)
class TestPostUser(CommonTests):
    """Test the responses items."""

    def test_minimal_keys(self, response):
        """Test the response item contains the minimal keys."""
        assert "id" in response.json
        assert "created_at" in response.json
        assert "subject" in response.json
        assert "issuer" in response.json
        assert "email" in response.json
        assert "drift_ids" in response.json

    def test_values_types(self, response):
        """Test the response item correct types."""
        assert isinstance(response.json["id"], str)
        assert isinstance(response.json["created_at"], str)
        assert isinstance(response.json["subject"], str)
        assert isinstance(response.json["issuer"], str)
        assert isinstance(response.json["email"], str)
        assert isinstance(response.json["drift_ids"], list)

    def test_drifts_empty(self, response):
        """Test user is created with no associated drifts."""
        assert response.json["drift_ids"] == []
