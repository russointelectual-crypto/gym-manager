"""Load reproducible demonstration data."""
import sys
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from flask_appbuilder import Model

from app import app, db
from app.models import Client, Discipline, Enrollment, Membership, Sale, Trainer

with app.app_context():
    Model.metadata.create_all(db.engine)
    if db.session.query(Client).count():
        print("La base ya contiene datos. No se duplicó la carga.")
        raise SystemExit(0)

    trainer_a = Trainer(full_name="María Quispe", specialty="Entrenamiento funcional", phone="70000001", email="maria@gym.local")
    trainer_b = Trainer(full_name="Carlos Rojas", specialty="Fuerza y musculación", phone="70000002", email="carlos@gym.local")
    db.session.add_all([trainer_a, trainer_b])
    db.session.flush()

    disciplines = [
        Discipline(name="Entrenamiento funcional", category="Funcional", schedule="Lun-Mié 07:00", capacity=20, monthly_fee=Decimal("180.00"), description="Circuitos, movilidad y resistencia para mejorar condición física.", trainer=trainer_a),
        Discipline(name="Musculación", category="Fuerza", schedule="Lun-Vie 18:00", capacity=25, monthly_fee=Decimal("220.00"), description="Fuerza, hipertrofia y técnica con pesas.", trainer=trainer_b),
        Discipline(name="Yoga", category="Bienestar", schedule="Mar-Jue 08:00", capacity=15, monthly_fee=Decimal("160.00"), description="Flexibilidad, respiración, equilibrio y reducción de estrés.", trainer=trainer_a),
        Discipline(name="Spinning", category="Cardio", schedule="Mar-Jue 19:00", capacity=18, monthly_fee=Decimal("190.00"), description="Cardio de alta energía para resistencia y quema de calorías.", trainer=trainer_b),
    ]
    db.session.add_all(disciplines)

    clients = [
        Client(full_name="Ana Flores", email="ana@example.com", phone="76543210", birth_date=date(1995, 4, 10), goal="Quiero perder peso y mejorar mi resistencia", status="Activo"),
        Client(full_name="Diego Mamani", email="diego@example.com", phone="76543211", birth_date=date(1991, 8, 5), goal="Ganar fuerza y masa muscular", status="Activo"),
        Client(full_name="Lucía Vargas", email="lucia@example.com", phone="76543212", birth_date=date(1988, 1, 25), goal="Reducir estrés y mejorar flexibilidad", status="Activo"),
    ]
    db.session.add_all(clients)
    db.session.flush()

    today = date.today()
    memberships = [
        Membership(client=clients[0], plan_name="Plan Estándar", start_date=today - timedelta(days=10), end_date=today + timedelta(days=20), status="Activa", monthly_fee=Decimal("250.00")),
        Membership(client=clients[1], plan_name="Plan Premium", start_date=today - timedelta(days=3), end_date=today + timedelta(days=27), status="Activa", monthly_fee=Decimal("350.00")),
        Membership(client=clients[2], plan_name="Plan Estándar", start_date=today - timedelta(days=40), end_date=today - timedelta(days=10), status="Vencida", monthly_fee=Decimal("250.00")),
    ]
    db.session.add_all(memberships)
    db.session.flush()
    db.session.add_all([
        Enrollment(client=clients[0], discipline=disciplines[0], status="Activa", notes="Objetivo de resistencia"),
        Enrollment(client=clients[1], discipline=disciplines[1], status="Activa", notes="Rutina de fuerza"),
        Enrollment(client=clients[2], discipline=disciplines[2], status="Activa", notes="Sesiones de bienestar"),
    ])
    db.session.add_all([
        Sale(client=clients[0], membership=memberships[0], concept="Membresía mensual", amount=Decimal("250.00"), sale_date=today - timedelta(days=5), payment_method="QR"),
        Sale(client=clients[1], membership=memberships[1], concept="Membresía premium", amount=Decimal("350.00"), sale_date=today - timedelta(days=2), payment_method="Tarjeta"),
        Sale(client=clients[2], membership=memberships[2], concept="Renovación vencida", amount=Decimal("250.00"), sale_date=today - timedelta(days=35), payment_method="Efectivo"),
    ])
    db.session.commit()
    print("Datos de demostración cargados correctamente.")
