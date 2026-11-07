"""Gym Manager application entry point."""
from flask import Flask
from flask_appbuilder import AppBuilder
from flask_appbuilder.models.sqla.base import SQLA

import config

app = Flask(__name__)
app.config.from_object(config)
db = SQLA(app)
appbuilder = AppBuilder()

# Flask-AppBuilder's security manager and blueprints need an active context
# during initialization. Keeping registration here also avoids circular setup.
with app.app_context():
    appbuilder.init_app(app, db.session)
    # Flask-AppBuilder 5.3 exposes the database login under this blueprint
    # endpoint while Flask-Login's default remains the legacy ``login`` name.
    appbuilder.sm.lm.login_view = "AuthDBView.login"
    from app import models  # noqa: E402,F401
    from app import views  # noqa: E402,F401
    from app import ai  # noqa: E402,F401
    from app import reports  # noqa: E402,F401


@app.context_processor
def inject_project_info():
    return {"project_name": app.config.get("APP_NAME", "Gym Manager")}
