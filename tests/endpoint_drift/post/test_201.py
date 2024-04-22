"""Testing module for endpoint methods /drift."""

# pylint: disable=redefined-outer-name
import uuid
from datetime import datetime as dt

from pytest import mark


@mark.parametrize("auth", ["mock-token"], indirect=True)
@mark.parametrize("with_database", ["database_1"], indirect=True)
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

    def test_drift_id(self, response):
        """Test the response item have correct id."""
        assert uuid.UUID(response.json["id"]).version == 4

    def test_datetime(self, response):
        """Test the response item has a correct date."""
        assert dt.fromisoformat(response.json["datetime"])

    def test_subset(self, response, body):
        """Test the response includes the body."""
        assert set(body).issubset(set(response.json))

    def test_user_drifts(self, response, db_user):
        """Test the drift id is in the user drifts."""
        assert response.json["id"] in db_user["drift_ids"]


# @mark.parametrize("schema_version", ["1.0.0"], indirect=True)
class TestPostDriftV100(CommonTests):
    """Test the responses items."""

    def test_version(self, response):
        """Test the response item has the correct version."""
        assert response.json["schema_version"] == "1.0.0"

    def test_minimal_keys(self, response):
        """Test the response item contains the minimal keys."""
        assert "id" in response.json
        assert "schema_version" in response.json
        assert "datetime" in response.json
        assert "job_status" in response.json
        assert "model" in response.json
        assert "concept_drift" in response.json
        assert "data_drift" in response.json

    def test_values_types(self, response):
        """Test the response item correct types."""
        assert isinstance(response.json["id"], str)
        assert isinstance(response.json["schema_version"], str)
        assert isinstance(response.json["datetime"], str)
        assert isinstance(response.json["job_status"], str)
        assert isinstance(response.json["model"], str)
        assert isinstance(response.json["concept_drift"], dict)
        assert isinstance(response.json["data_drift"], dict)

    @mark.parametrize(
        argnames="concept_drift",
        argvalues=[
            {"drift": True, "parameters": {"p_value": 0.1}},
            {"drift": True, "parameters": {"p_value": 0.1}},
        ],
        indirect=True,
    )
    def test_concept_drift(self, response, concept_drift):
        """Test the concept drift response."""
        assert response.json["concept_drift"] == concept_drift

    @mark.parametrize("concept_drift", [None], indirect=True)
    def test_no_concept_drift(self, response):
        """Test the no concept drift response."""
        no_drift = {"drift": False, "parameters": {}}
        assert response.json["concept_drift"] == no_drift

    @mark.parametrize(
        argnames="data_drift",
        argvalues=[
            {"drift": True, "parameters": {"p_value": 0.1}},
            {"drift": True, "parameters": {"p_value": 0.1}},
        ],
        indirect=True,
    )
    def test_data_drift(self, response, data_drift):
        """Test the data drift response."""
        assert response.json["data_drift"] == data_drift

    @mark.parametrize("data_drift", [None], indirect=True)
    def test_no_data_drift(self, response):
        """Test the no data drift response."""
        no_drift = {"drift": False, "parameters": {}}
        assert response.json["data_drift"] == no_drift
