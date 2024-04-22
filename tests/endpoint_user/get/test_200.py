"""Testing module for endpoint methods /user."""

# pylint: disable=redefined-outer-name
from datetime import datetime as dt

from pytest import mark


@mark.parametrize("auth", ["mock-token"], indirect=True)
@mark.parametrize("with_database", ["database_1"], indirect=True)
@mark.usefixtures("with_context", "with_database")
@mark.usefixtures("accept_authorization")
class CommonTests:
    """Common tests for the /user endpoint."""

    def test_status_code(self, response):
        """Test the 200 response."""
        assert response.status_code == 200

    def test_data_as_list(self, response):
        """Test response data is delivered as list."""
        assert isinstance(response.json, list)
        assert len(response.json) != 0

    def test_created_at(self, response):
        """Test the response items contain a correct date."""
        assert all(dt.fromisoformat(x["created_at"]) for x in response.json)


@mark.parametrize("entitlements", [["iam:admin"], ["iam:dev"]], indirect=True)
class TestGetUser(CommonTests):
    """Test the responses items."""

    def test_minimal_keys(self, response):
        """Test the response items contain the minimal keys."""
        assert all("id" in x for x in response.json)
        assert all("created_at" in x for x in response.json)
        assert all("subject" in x for x in response.json)
        assert all("issuer" in x for x in response.json)
        assert all("email" in x for x in response.json)
        assert all("drift_ids" in x for x in response.json)

    def test_values_types(self, response):
        """Test the response items contain the correct types."""
        assert all(isinstance(x["id"], str) for x in response.json)
        assert all(isinstance(x["created_at"], str) for x in response.json)
        assert all(isinstance(x["subject"], str) for x in response.json)
        assert all(isinstance(x["issuer"], str) for x in response.json)
        assert all(isinstance(x["email"], str) for x in response.json)
        assert all(isinstance(x["drift_ids"], list) for x in response.json)

    @mark.parametrize("created_after", ["2020-01-10"], indirect=True)
    def test_after_date(self, response, after_dateiso):
        """Test the response items are after the indicated date."""
        for item in response.json:
            assert dt.fromisoformat(item["created_at"]) >= after_dateiso

    @mark.parametrize("created_before", ["2020-01-20"], indirect=True)
    def test_before_date(self, response, before_dateiso):
        """Test the response items are before the indicated date."""
        for item in response.json:
            assert dt.fromisoformat(item["created_at"]) <= before_dateiso

    @mark.parametrize("issuer", ["issuer_1"], indirect=True)
    def test_issuer(self, response, issuer):
        """Test the response items contain the correct issuer."""
        assert all(x["issuer"] == issuer for x in response.json)

    @mark.parametrize(
        argnames="drift_ids",
        argvalues=[
            {
                "drift_ids": {
                    "$all": [
                        "00000000-0000-0001-0001-000000000001",
                        "00000000-0000-0001-0001-000000000002",
                    ]
                }
            },
        ],
        indirect=True,
    )
    def test_all_drift_ids(self, response, drift_ids):
        """Test the response items contain the drift ids."""
        for item in response.json:
            assert all(y in item["drift_ids"] for y in drift_ids)

    @mark.parametrize(
        argnames="drift_ids",
        argvalues=[
            {
                "drift_ids": {
                    "$in": [
                        "00000000-0000-0001-0001-000000000001",
                        "00000000-0000-0001-0001-000000000002",
                    ]
                }
            },
        ],
        indirect=True,
    )
    def test_any_drift_ids(self, response, drift_ids):
        """Test the response items contain the drift ids."""
        for item in response.json:
            assert any(y in item["drift_ids"] for y in drift_ids)
