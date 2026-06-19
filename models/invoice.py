from db.database import Base
from sqlalchemy import Identity, ForeignKey, String, Numeric, Integer, CheckConstraint, Enum as SQLEnum, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from decimal import Decimal
from datetime import date

from enums.order_status import OrderStatus
from enums.invoice_status import InvoiceStatus
from models import OrderLine, Customer, Order

class Invoice(Base):
    __tablename__ = "invoices"
    __table_args__ = (
        CheckConstraint("invoice_number > 0", name="ck_positive_invoice_number")
    )
    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    invoice_number: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    customer_id : Mapped[int] = mapped_column(ForeignKey("customers.id"))
    customer: Mapped["Customer"] = relationship("Customer", back_populates="invoices")
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    order: Mapped["Order"] = relationship("Order", back_populates="invoice")
    issue_date: Mapped[date] = mapped_column(Date, nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[OrderStatus] = mapped_column(SQLEnum(
                                            InvoiceStatus,
                                            name="status_enum",
                                            create_constraint=True
                                            ),
                                            nullable=False)


