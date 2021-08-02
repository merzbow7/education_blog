import pytest

from app import create_app, db
from unit_test.unit.unit_test import TestConfig


@pytest.fixture(scope="session")
def init_app():
    return create_app(TestConfig)


@pytest.fixture()
def init_db(init_app):
    app_context = init_app.app_context()
    app_context.push()
    db.create_all()

    yield db

    db.session.remove()
    db.drop_all()
    app_context.pop()

