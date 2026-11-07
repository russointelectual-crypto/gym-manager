"""Create database tables without deleting existing data."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from flask_appbuilder import Model

from app import app, db

with app.app_context():
    Model.metadata.create_all(db.engine)
    print(f"Base de datos preparada: {app.config['SQLALCHEMY_DATABASE_URI']}")
