from db.database import Base
from sqlalchemy import Identity, ForeignKey, Integer, CheckConstraint, Enum as SQLEnum, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from datetime import date
from typing import TYPE_CHECKING

from enums.invoice_status import InvoiceStatus
if TYPE_CHECKING:
    from models import Customer, Order, InvoiceLine



class Invoice(Base):
    __tablename__ = "invoices"
    __table_args__ = (
        CheckConstraint("invoice_number > 0", name="ck_positive_invoice_number"),
        CheckConstraint("due_date >= issue_date", name="ck_due_after_issue_date")
    )
    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    invoice_number: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    customer_id : Mapped[int] = mapped_column(ForeignKey("customers.id"))
    customer: Mapped["Customer"] = relationship("Customer", back_populates="invoices")
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), unique=True)
    order: Mapped["Order"] = relationship("Order", back_populates="invoice")
    issue_date: Mapped[date] = mapped_column(Date, nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[InvoiceStatus] = mapped_column(SQLEnum(
                                            InvoiceStatus,
                                            name="invoice_status_enum",
                                            create_constraint=True
                                            ),
                                            nullable=False)
    invoice_lines: Mapped[list["InvoiceLine"]] = relationship("InvoiceLine", back_populates="invoice", cascade="all, delete-orphan")

    @validates("due_date")
    def validate_issue_date(self, key, due_date, issue_date):
        if self.issue_date is not None and due_date < self.issue_date:
            raise ValueError("Incorrect value: Due date cannot be earlier than issue date")
        return due_date


