from db.database import Base
from sqlalchemy import Identity, ForeignKey, String, Numeric, Integer, CheckConstraint, Enum as SQLEnum, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from decimal import Decimal
from datetime import date
from typing import TYPE_CHECKING

from enums.order_status import OrderStatus
if TYPE_CHECKING:
    from models import Product, Order, Invoice

class InvoiceLine(Base):
    __tablename__ = "invoice_lines"
    __table_args__ = (
    )
    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    invoice_id: Mapped[int] = mapped_column(ForeignKey("invoices.id"))
    invoice: Mapped["Invoice"] = relationship("Invoice", back_populates="invoice_lines")
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)
    vat_rate: Mapped[Decimal] = mapped_column(Numeric(5,2), nullable=False)