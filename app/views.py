"""CRUD views and business validations for Flask-AppBuilder."""
from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from sqlalchemy import func

from app import appbuilder, db
from app.models import Client, Discipline, Enrollment, Membership, Sale, Trainer


class SecureModelView(ModelView):
    """Shared CRUD behavior with clear user-facing validation messages."""
    page_size = 20

    def pre_add(self, item):
        self._validate_business_rules(item)

    def pre_update(self, item):
        self._validate_business_rules(item)

    def _validate_business_rules(self, item):
        if isinstance(item, Client):
            if "@" not in item.email:
                raise ValueError("El correo del cliente debe tener un formato válido.")
        if isinstance(item, Discipline) and item.capacity <= 0:
            raise ValueError("La capacidad debe ser mayor que cero.")
        if isinstance(item, Membership) and item.end_date < item.start_date:
            raise ValueError("La fecha de fin no puede ser anterior a la fecha de inicio.")
        if isinstance(item, Sale) and item.amount <= 0:
            raise ValueError("El monto de la venta debe ser mayor que cero.")


class ClientModelView(SecureModelView):
    datamodel = SQLAInterface(Client)
    list_columns = ["full_name", "email", "phone", "goal", "status", "created_at"]
    add_columns = ["full_name", "email", "phone", "birth_date", "goal", "status"]
    edit_columns = add_columns
    show_columns = ["full_name", "email", "phone", "birth_date", "goal", "status", "created_at", "memberships", "enrollments", "sales"]
    search_columns = ["full_name", "email", "phone", "status"]
    label_columns = {"full_name": "Nombre completo", "birth_date": "Fecha de nacimiento", "created_at": "Registrado"}


class TrainerModelView(SecureModelView):
    datamodel = SQLAInterface(Trainer)
    list_columns = ["full_name", "specialty", "phone", "email", "active"]
    add_columns = ["full_name", "specialty", "phone", "email", "active"]
    edit_columns = add_columns
    show_columns = ["full_name", "specialty", "phone", "email", "active", "disciplines"]
    search_columns = ["full_name", "specialty", "active"]


class DisciplineModelView(SecureModelView):
    datamodel = SQLAInterface(Discipline)
    list_columns = ["name", "category", "schedule", "capacity", "monthly_fee", "trainer"]
    add_columns = ["name", "category", "schedule", "capacity", "monthly_fee", "description", "trainer"]
    edit_columns = add_columns
    show_columns = ["name", "category", "schedule", "capacity", "monthly_fee", "description", "trainer", "enrollments"]
    search_columns = ["name", "category", "schedule", "trainer"]


class MembershipModelView(SecureModelView):
    datamodel = SQLAInterface(Membership)
    list_columns = ["client", "plan_name", "start_date", "end_date", "status", "monthly_fee"]
    add_columns = ["client", "plan_name", "start_date", "end_date", "status", "monthly_fee"]
    edit_columns = add_columns
    show_columns = ["client", "plan_name", "start_date", "end_date", "status", "monthly_fee", "sales"]
    search_columns = ["client", "plan_name", "status"]


class EnrollmentModelView(SecureModelView):
    datamodel = SQLAInterface(Enrollment)
    list_columns = ["client", "discipline", "enrolled_on", "status", "notes"]
    add_columns = ["client", "discipline", "enrolled_on", "status", "notes"]
    edit_columns = add_columns
    show_columns = add_columns
    search_columns = ["client", "discipline", "status"]

    def pre_add(self, item):
        super().pre_add(item)
        if item.client and item.discipline:
            active_count = (
                db.session.query(func.count(Enrollment.id))
                .filter(Enrollment.discipline_id == item.discipline_id, Enrollment.status == "Activa")
                .scalar()
            )
            duplicate = db.session.query(Enrollment.id).filter_by(client_id=item.client_id, discipline_id=item.discipline_id).first()
            if duplicate:
                raise ValueError("El cliente ya está inscrito en esta disciplina.")
            if active_count >= item.discipline.capacity:
                raise ValueError("La disciplina alcanzó su capacidad máxima.")


class SaleModelView(SecureModelView):
    datamodel = SQLAInterface(Sale)
    list_columns = ["sale_date", "client", "concept", "amount", "payment_method", "status"]
    add_columns = ["client", "membership", "concept", "amount", "sale_date", "payment_method", "status"]
    edit_columns = add_columns
    show_columns = add_columns
    search_columns = ["client", "concept", "payment_method", "status"]


appbuilder.add_view(ClientModelView, "Clientes", icon="fa-user", category="Gestión")
appbuilder.add_view(TrainerModelView, "Entrenadores", icon="fa-id-badge", category="Gestión")
appbuilder.add_view(DisciplineModelView, "Disciplinas", icon="fa-heartbeat", category="Gestión")
appbuilder.add_view(MembershipModelView, "Membresías", icon="fa-credit-card", category="Gestión")
appbuilder.add_view(EnrollmentModelView, "Inscripciones", icon="fa-calendar-check-o", category="Gestión")
appbuilder.add_view(SaleModelView, "Ventas", icon="fa-money", category="Gestión")
