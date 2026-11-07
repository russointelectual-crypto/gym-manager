"""Create or update the administrator account from environment variables."""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from werkzeug.security import generate_password_hash
from flask_appbuilder import Model

from app import app, appbuilder, db

with app.app_context():
    Model.metadata.create_all(db.engine)
    username = os.getenv("ADMIN_USERNAME", "admin")
    password = os.getenv("ADMIN_PASSWORD", "Admin123!")
    role = appbuilder.sm.find_role("Admin")
    user = appbuilder.sm.find_user(username=username)
    if user:
        user.password = generate_password_hash(password)
        user.roles = [role] if role else user.roles
        print(f"Cuenta actualizada: {username}")
    else:
        user = appbuilder.sm.add_user(
            username=username,
            first_name=os.getenv("ADMIN_FIRST_NAME", "Administrador"),
            last_name=os.getenv("ADMIN_LAST_NAME", "Sistema"),
            email=os.getenv("ADMIN_EMAIL", "admin@gym.local"),
            role=role,
            password=password,
        )
        print(f"Cuenta creada: {username}")
    db.session.commit()
