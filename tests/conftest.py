"""Pytest configuration for testing the backend."""

# pylint: disable=redefined-outer-name
import os

import requests
from pytest import fixture


@fixture(scope="session")
def endpoint():
    """Return the base URL for the API."""
    return os.environ["APP_DOMAIN_NAME"]


@fixture(scope="class", name="response")
def request(endpoint, path, query, body):
    """Create a request object."""
    yield requests.get(
        url=f"https://{endpoint}/{path}",
        params=query,
        json=body,
        timeout=5,
        verify=False,
    )


@fixture(scope="class")
def query(request):
    """Create a request query."""
    return request.param


@fixture(scope="class")
def body(request):
    """Create a request body."""
    return request.param
