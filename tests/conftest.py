import os

# Use an isolated SQLite database for automated tests.
os.environ["DATABASE_URL"] = "sqlite:///test_gym_manager.sqlite3"
os.environ["SECRET_KEY"] = "test-secret"
os.environ["FLASK_DEBUG"] = "0"

import pytest
from flask_appbuilder import Model

from app import app, db


@pytest.fixture()
def client():
    app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
    with app.app_context():
        Model.metadata.drop_all(db.engine)
        Model.metadata.create_all(db.engine)
    with app.test_client() as test_client:
        yield test_client
    with app.app_context():
        db.session.remove()
        Model.metadata.drop_all(db.engine)
