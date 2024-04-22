"""Pytest configuration for testing the backend."""

# pylint: disable=redefined-outer-name
import json
import os
import uuid

import marshmallow as ma
from flaat.user_infos import UserInfos
from pytest import fixture
from werkzeug.datastructures import Authorization

from backend.app import create_app, schemas
from backend.app.tools import authentication


@fixture(scope="session")
def app():
    """Create and configure a new app instance for each test."""
    # See: https://flask.palletsprojects.com/en/3.0.x/testing/
    app = create_app()
    app.config.update({"TESTING": True})
    # other setup tasks can go here
    yield app
    # clean up after the test run


@fixture(scope="module", autouse=True)
def patch_database(app):
    """Patch the database connection."""
    db_client = app.config["db_client"]
    db_name = f"test-db-{uuid.uuid4()}"
    app.config.update({"db": db_client[db_name]})
    yield
    db_client.drop_database(app.config["db"])


@fixture(scope="module")
def database(app):
    """Return the database from the application."""
    return app.config["db"]


@fixture(scope="module")
def with_database(request, database):
    """Loads the database with data from data file."""
    if hasattr(request, "param") and request.param:
        sandbox_path = os.environ.get("TESTS_DATABASE_SANDBOX")
        file_path = f"{sandbox_path}/{request.param}.json"
        with open(file_path, "r", encoding="utf-8") as file:
            for section in json.load(file):
                load_section(section, database)


def load_section(section, database):
    """Load a section of the database."""
    serializer = schemas.__dict__[section["schema"]]
    serializer = serializer(many=True, unknown=ma.INCLUDE)
    items = serializer.load(section["items"])
    if items:
        database[section["collection"]].insert_many(items)


@fixture(scope="module")
def client(app):
    return app.test_client()


@fixture(scope="module")
def with_context(app):
    with app.app_context() as context:
        yield context


@fixture(scope="class")
def request_kwds(request, auth, query, body):
    """Create a request kwds dict to complete."""
    kwds = {"query_string": query, "json": body, "auth": auth}
    kwds.update(request.param if hasattr(request, "param") else {})
    return kwds


@fixture(scope="class")
def auth(request):
    """Inject and return a request auth."""
    if request.param is None:
        return None
    return Authorization("bearer", token=request.param)


@fixture(scope="class")
def query(request):
    """Inject and return a request query."""
    return request.param if hasattr(request, "param") else None


@fixture(scope="class")
def body(request):
    """Inject and return a request body."""
    return request.param if hasattr(request, "param") else None


@fixture(scope="class")
def subiss(request):
    """Inject and return a request subiss."""
    if not hasattr(request, "param"):
        return "user_1", "issuer_1"
    return request.param


@fixture(scope="class")
def entitlements(request):
    """Inject and return a request entitlements."""
    return request.param if hasattr(request, "param") else []


@fixture(scope="class")
def email(request, subiss):
    """Inject and return a request email."""
    if not hasattr(request, "param"):
        return f"{subiss[0]}@{subiss[1]}.com"
    return request.param


@fixture(scope="class")
def accept_authorization(class_mocker, subiss, email, entitlements):
    """Patches flaat to edit provided user_infos."""
    user_info = {
        "email": email,
        "email_verified": bool(email) and email != "bad-email",
        "sub": subiss[0],
        "iss": subiss[1],
        "eduperson_entitlement": entitlements,
    }
    class_mocker.patch.object(
        authentication.flaat,
        "get_user_infos_from_access_token",
        return_value=UserInfos(
            access_token_info=None,
            user_info=user_info,
            introspection_info=None,
        ),
    )


@fixture(scope="class")
def db_user(response, database, subiss):
    """Returns user from database after response."""
    db_filter = {"subject": subiss[0], "issuer": subiss[1]}
    user = database["app.blueprints.user"].find_one(db_filter)
    if user is not None:
        user["id"] = user.pop("_id")
    return user


@fixture(scope="class")
def grant_admin(monkeypatch):
    """Patch fixture to test function as admin user."""
    admin_assert = authentication.flaat.access_levels[1].requirement
    monkeypatch.setattr(admin_assert, "func", lambda *args: True)
