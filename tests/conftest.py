"""Pytest configuration for testing the backend."""

# pylint: disable=redefined-outer-name
import os

import requests
from pymongo import MongoClient
from pytest import fixture


@fixture(scope="session")
def db_client():
    """Return a MongoDB client."""
    # Secret from sandbox, do not use same in production
    return MongoClient(
        host=os.getenv("APP_DATABASE_HOST", "localhost"),
        port=int(os.getenv("APP_DATABASE_PORT", "27017")),
        username=os.getenv("APP_DATABASE_USERNAME", "user-default"),
        password="4a9ac8715296c9fbc91efa5216bf6814",
    )


@fixture(scope="session")
def db(db_client):
    """Return the database."""
    return db_client["test-data"]


@fixture(scope="session")
def endpoint():
    """Return the base URL for the API."""
    return os.environ["APP_DOMAIN_NAME"]


@fixture(scope="class", name="response")
def request(endpoint, path, query, body):
    """Create a request object."""
    yield requests.post(
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
