"""Testing module for endpoint methods /drift."""

# pylint: disable=redefined-outer-name


def test_creation(db, experiment):
    """Test the properties of the monitor."""
    experiment = db["app.experiments"].find_one({"name": experiment.name})
    assert experiment is not None
