from db.database import Base
from sqlalchemy import Identity, ForeignKey, String, Numeric, Integer, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy.ext.hybrid import hybrid_property
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Order, Invoice

class Customer(Base):
    __tablename__ = "customers"
    __table_args__ = (
        CheckConstraint("length(vat_number) >= 8", name="ck_vat_number_length"),
        UniqueConstraint("vat_number", name="uq_customers_vat_number")
    )
    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(75), nullable=False)
    vat_number: Mapped[str] = mapped_column(String(50), nullable=False)
    address: Mapped[str | None] = mapped_column(String, nullable=True)
    orders: Mapped[list["Order"]] = relationship(back_populates="customer")
    invoices: Mapped[list["Invoice"]] = relationship(back_populates="customer")

    @hybrid_property
    def customer_number(self):
        return f"C-{self.id:06d}"

    @validates("vat_number")
    def validate_vat_number(self, key, vat_number):
        #maybe add validator on EU country ?
        if len(vat_number) < 8:
            raise ValueError("Incorrect value : VAT Number must be at least 8 characters long")
        return vat_number