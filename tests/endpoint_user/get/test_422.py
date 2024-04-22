"""Testing module for endpoint methods /drift."""

# pylint: disable=redefined-outer-name
from pytest import mark, fixture


@mark.parametrize("auth", ["mock-token"], indirect=True)
@mark.parametrize("entitlements", [["iam:admin"]], indirect=True)
@mark.usefixtures("accept_authorization")
class CommonTests:
    """Common tests for the /drift endpoint."""

    @fixture(scope="class")
    def body(self, request):
        """Inject and return a request body."""
        return request.param

    def test_status_code(self, response):
        """Test the 422 response."""
        assert response.status_code == 422


@mark.parametrize("body", ["string_body"], indirect=True)
class TestBadBody(CommonTests):
    """Test the bad_key parameter."""

    def test_error_msg(self, response):
        """Test message contains useful information."""
        assert "_schema" in response.json["errors"]["json"]
        error = response.json["errors"]["json"]["_schema"]
        assert error == ["Invalid input type."]
