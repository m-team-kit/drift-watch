"""Testing module for endpoint methods /drift."""

# pylint: disable=redefined-outer-name
from datetime import datetime as dt

from pytest import mark


@mark.parametrize("auth", [None], indirect=True)
@mark.parametrize("with_database", ["database_1"], indirect=True)
@mark.usefixtures("with_context", "with_database")
class CommonTests:
    """Common tests for the /drift endpoint."""

    def test_status_code(self, response):
        """Test the 200 response."""
        assert response.status_code == 200

    def test_data_as_list(self, response):
        """Test response data is delivered as list."""
        assert isinstance(response.json, list)
        assert len(response.json) != 0

    def test_versions(self, response, schema_version):
        """Test the response items contain the correct version."""
        sv = schema_version
        assert all(x["schema_version"] == sv for x in response.json)


class DatetimeTests(CommonTests):
    """Test the response items datetime."""

    def test_datetime(self, response):
        """Test the response items contain a correct date."""
        assert all(dt.fromisoformat(x["datetime"]) for x in response.json)

    @mark.parametrize("start_date", ["2020-01-10"], indirect=True)
    def test_after_date(self, response, start_dateiso):
        """Test the response items are after the indicated date."""
        for item in response.json:
            assert dt.fromisoformat(item["datetime"]) >= start_dateiso

    @mark.parametrize("end_date", ["2020-01-20"], indirect=True)
    def test_before_date(self, response, end_dateiso):
        """Test the response items are before the indicated date."""
        for item in response.json:
            assert dt.fromisoformat(item["datetime"]) <= end_dateiso


class StatusTests(CommonTests):
    """Test the response items job status."""

    @mark.parametrize(
        argnames="job_status",
        argvalues=["Running", "Completed", "Failed"],
        indirect=True,
    )
    def test_job_status(self, response, job_status):
        """Test the job status is correctly updated."""
        assert all(x["job_status"] == job_status for x in response.json)


@mark.parametrize("schema_version", ["1.0.0"], indirect=True)
class TestGetDriftV100(DatetimeTests, StatusTests, CommonTests):
    """Test the responses items."""

    def test_minimal_keys(self, response):
        """Test the response items contain the minimal keys."""
        assert all("id" in x for x in response.json)
        assert all("schema_version" in x for x in response.json)
        assert all("datetime" in x for x in response.json)
        assert all("model" in x for x in response.json)
        assert all("concept_drift" in x for x in response.json)
        assert all("data_drift" in x for x in response.json)

    def test_values_types(self, response):
        """Test the response items contain the correct types."""
        assert all(isinstance(x["id"], str) for x in response.json)
        assert all(isinstance(x["schema_version"], str) for x in response.json)
        assert all(isinstance(x["datetime"], str) for x in response.json)
        assert all(isinstance(x["model"], str) for x in response.json)
        assert all(isinstance(x["concept_drift"], dict) for x in response.json)
        assert all(isinstance(x["data_drift"], dict) for x in response.json)

    @mark.parametrize("model", ["model_1"], indirect=True)
    def test_model(self, response, model):
        """Test the response items contain the correct model."""
        assert all(x["model"] == model for x in response.json)

    @mark.parametrize("concept_drift", [{"$exists": True}], indirect=True)
    def test_concept_drift(self, response):
        """Test the response items concept drift."""
        assert all("concept_drift" in item for item in response.json)

    @mark.parametrize("data_drift", [{"$exists": True}], indirect=True)
    def test_data_drift(self, response):
        """Test the response items data drift."""
        assert all("data_drift" in item for item in response.json)
