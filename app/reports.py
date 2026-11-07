"""Database-backed reports with GET filters."""
from datetime import date, timedelta
from decimal import Decimal

from flask import request
from flask_appbuilder import BaseView, expose, has_access
from sqlalchemy import func

from app import appbuilder, db
from app.models import Client, Discipline, Enrollment, Membership, Sale


def parse_date(value, fallback):
    try:
        return date.fromisoformat(value) if value else fallback
    except ValueError:
        return fallback


class ReportsView(BaseView):
    route_base = "/reports"
    default_view = "sales"

    @expose("/sales")
    @has_access
    def sales(self):
        start = parse_date(request.args.get("start"), date.today() - timedelta(days=30))
        end = parse_date(request.args.get("end"), date.today())
        payment_method = request.args.get("payment_method", "")
        query = db.session.query(Sale).filter(Sale.sale_date.between(start, end))
        if payment_method:
            query = query.filter(Sale.payment_method == payment_method)
        rows = query.order_by(Sale.sale_date.desc(), Sale.id.desc()).all()
        total = sum((sale.amount for sale in rows), Decimal("0.00"))
        return self.render_template(
            "reports/sales.html", rows=rows, total=total, start=start, end=end,
            payment_method=payment_method,
        )

    @expose("/memberships")
    @has_access
    def memberships(self):
        status = request.args.get("status", "")
        query = (
            db.session.query(
                Membership.plan_name,
                Membership.status,
                func.count(Membership.id).label("members"),
                func.coalesce(func.sum(Membership.monthly_fee), 0).label("monthly_revenue"),
            )
            .group_by(Membership.plan_name, Membership.status)
            .order_by(Membership.plan_name, Membership.status)
        )
        if status:
            query = query.filter(Membership.status == status)
        rows = query.all()
        return self.render_template("reports/memberships.html", rows=rows, status=status)

    @expose("/occupancy")
    @has_access
    def occupancy(self):
        rows = (
            db.session.query(
                Discipline.name,
                Discipline.category,
                Discipline.capacity,
                func.count(Enrollment.id).label("enrolled"),
                TrainerName.full_name.label("trainer_name"),
            )
            .outerjoin(Enrollment, (Enrollment.discipline_id == Discipline.id) & (Enrollment.status == "Activa"))
            .join(TrainerName, Discipline.trainer_id == TrainerName.id)
            .group_by(Discipline.id, Discipline.name, Discipline.category, Discipline.capacity, TrainerName.full_name)
            .order_by(Discipline.name)
            .all()
        )
        return self.render_template("reports/occupancy.html", rows=rows)


# Alias kept local to make the report query readable while retaining only six
# domain tables. It is imported lazily after model declarations.
from app.models import Trainer as TrainerName  # noqa: E402

appbuilder.add_view(ReportsView(), "Reportes", icon="fa-bar-chart", category="Análisis")
