"""Configuration for the Gym Manager Flask-AppBuilder project."""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def _database_uri() -> str:
    """Use MySQL when DATABASE_URL is supplied and SQLite for a quick demo."""
    return os.getenv(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR / 'gym_manager.db'}",
    )


SECRET_KEY = os.getenv("SECRET_KEY", "development-only-change-me")
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"
SQLALCHEMY_DATABASE_URI = _database_uri()
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_pre_ping": True,
}

# Flask-AppBuilder authentication and security defaults.
AUTH_TYPE = 1  # AUTH_DB
AUTH_ROLE_ADMIN = "Admin"
AUTH_USER_REGISTRATION = False
AUTH_USER_REGISTRATION_ROLE = "Public"
AUTH_USERNAME_CI = True
FAB_API_MAX_PAGE_SIZE = 500
APP_NAME = "Gym Manager"
