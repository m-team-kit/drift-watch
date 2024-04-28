"""Testing module for endpoint methods /drift."""

# pylint: disable=redefined-outer-name
from pytest import mark


@mark.parametrize("query", [{"page": 1, "page_size": 2}], indirect=True)
@mark.parametrize("body", [{}], indirect=True)
def test_simple(response):
    """Test the response."""
    assert response.status_code == 200
    assert len(response.json()) == 2
