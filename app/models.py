"""Domain models for the gym management system."""
from datetime import date, datetime
from decimal import Decimal

from flask_appbuilder import Model
from sqlalchemy import CheckConstraint, Date, DateTime, ForeignKey, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from app import db


class Client(Model):
    __tablename__ = "clients"
    __table_args__ = (UniqueConstraint("email", name="uq_client_email"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(160), nullable=False, index=True)
    phone: Mapped[str] = mapped_column(String(30), nullable=False)
    birth_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    goal: Mapped[str] = mapped_column(String(200), nullable=False, default="Mejorar mi condición física")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="Activo")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    memberships: Mapped[list["Membership"]] = relationship(back_populates="client", cascade="all, delete-orphan")
    enrollments: Mapped[list["Enrollment"]] = relationship(back_populates="client", cascade="all, delete-orphan")
    sales: Mapped[list["Sale"]] = relationship(back_populates="client", cascade="all, delete-orphan")

    @validates("email")
    def normalize_email(self, key, value):
        return value.strip().lower()

    def __repr__(self):
        return self.full_name


class Trainer(Model):
    __tablename__ = "trainers"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    specialty: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String(160), nullable=False)
    active: Mapped[bool] = mapped_column(default=True, nullable=False)

    disciplines: Mapped[list["Discipline"]] = relationship(back_populates="trainer")

    def __repr__(self):
        return self.full_name


class Discipline(Model):
    __tablename__ = "disciplines"
    __table_args__ = (
        UniqueConstraint("name", name="uq_discipline_name"),
        CheckConstraint("capacity > 0", name="ck_discipline_capacity_positive"),
        CheckConstraint("monthly_fee >= 0", name="ck_discipline_fee_nonnegative"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(80), nullable=False)
    schedule: Mapped[str] = mapped_column(String(120), nullable=False)
    capacity: Mapped[int] = mapped_column(nullable=False, default=20)
    monthly_fee: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    trainer_id: Mapped[int] = mapped_column(ForeignKey("trainers.id"), nullable=False)

    trainer: Mapped[Trainer] = relationship(back_populates="disciplines")
    enrollments: Mapped[list["Enrollment"]] = relationship(back_populates="discipline", cascade="all, delete-orphan")

    def __repr__(self):
        return self.name


class Membership(Model):
    __tablename__ = "memberships"
    __table_args__ = (CheckConstraint("end_date >= start_date", name="ck_membership_dates"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), nullable=False)
    plan_name: Mapped[str] = mapped_column(String(80), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="Activa")
    monthly_fee: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)

    client: Mapped[Client] = relationship(back_populates="memberships")
    sales: Mapped[list["Sale"]] = relationship(back_populates="membership")

    def __repr__(self):
        return f"{self.plan_name} - {self.client.full_name if self.client else self.client_id}"


class Enrollment(Model):
    __tablename__ = "enrollments"
    __table_args__ = (UniqueConstraint("client_id", "discipline_id", name="uq_client_discipline"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), nullable=False)
    discipline_id: Mapped[int] = mapped_column(ForeignKey("disciplines.id"), nullable=False)
    enrolled_on: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="Activa")
    notes: Mapped[str] = mapped_column(Text, nullable=False, default="")

    client: Mapped[Client] = relationship(back_populates="enrollments")
    discipline: Mapped[Discipline] = relationship(back_populates="enrollments")

    def __repr__(self):
        return f"{self.client.full_name if self.client else self.client_id} - {self.discipline.name if self.discipline else self.discipline_id}"


class Sale(Model):
    __tablename__ = "sales"
    __table_args__ = (CheckConstraint("amount > 0", name="ck_sale_amount_positive"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), nullable=False)
    membership_id: Mapped[int | None] = mapped_column(ForeignKey("memberships.id"), nullable=True)
    concept: Mapped[str] = mapped_column(String(160), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    sale_date: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)
    payment_method: Mapped[str] = mapped_column(String(30), nullable=False, default="Efectivo")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="Pagada")

    client: Mapped[Client] = relationship(back_populates="sales")
    membership: Mapped[Membership | None] = relationship(back_populates="sales")

    def __repr__(self):
        return f"{self.concept} - Bs {self.amount}"
