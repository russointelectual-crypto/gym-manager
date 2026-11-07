from datetime import date, timedelta
from decimal import Decimal

from app import db
from app.ai import recommend_disciplines
from app.models import Client, Discipline, Enrollment, Membership, Sale, Trainer


def seed_small_dataset():
    trainer = Trainer(full_name="Test Trainer", specialty="Fuerza", phone="70000000", email="trainer@test.local")
    client = Client(full_name="Test Client", email="client@test.local", phone="70000001", goal="Ganar fuerza y masa muscular", status="Activo")
    db.session.add_all([trainer, client])
    db.session.flush()
    disciplines = [
        Discipline(name="Fuerza", category="Fuerza", schedule="Lun", capacity=10, monthly_fee=Decimal("100"), description="fuerza masa muscular", trainer=trainer),
        Discipline(name="Yoga", category="Bienestar", schedule="Mar", capacity=10, monthly_fee=Decimal("100"), description="flexibilidad y respiracion", trainer=trainer),
    ]
    db.session.add_all(disciplines)
    db.session.commit()
    return client, trainer, disciplines


def test_database_relationships_and_ai(client):
    with client.application.app_context():
        customer, _, disciplines = seed_small_dataset()
        membership = Membership(client=customer, plan_name="Estándar", start_date=date.today(), end_date=date.today() + timedelta(days=30), status="Activa", monthly_fee=Decimal("100"))
        enrollment = Enrollment(client=customer, discipline=disciplines[0], status="Activa")
        sale = Sale(client=customer, membership=membership, concept="Membresía", amount=Decimal("100"), payment_method="QR")
        db.session.add_all([membership, enrollment, sale])
        db.session.commit()
        loaded = db.session.get(Client, customer.id)
        assert loaded.memberships[0].plan_name == "Estándar"
        assert loaded.enrollments[0].discipline.name == "Fuerza"
        assert loaded.sales[0].amount == Decimal("100.00")
        _, recommendations = recommend_disciplines(customer.id)
        assert recommendations
        assert recommendations[0][0].name == "Yoga"


def test_public_routes_and_reports_require_authentication(client):
    response = client.get("/reports/sales")
    assert response.status_code in (302, 401)
    response = client.get("/api/ai/recommendations/1")
    assert response.status_code in (302, 401, 404)
