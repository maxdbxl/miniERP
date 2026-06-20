from db.database import Base
from sqlalchemy import Identity, ForeignKey, String, Numeric, Integer, CheckConstraint, Enum as SQLEnum, Date, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from decimal import Decimal
from datetime import date
from typing import TYPE_CHECKING

from enums.order_status import OrderStatus
if TYPE_CHECKING:
    from models import Product, Order 

class OrderLine(Base):
    __tablename__ = "order_lines"
    __table_args__ = (
        CheckConstraint("unit_price >= 0", name="ck_positive_price"),
        CheckConstraint("quantity > 0", name="ck_positive_quantity"),
        CheckConstraint("vat_rate >= 0 AND vat_rate <= 1", name="ck_vat_rate"),
        UniqueConstraint("order_id", "product_id", name="uq_order_product"),
    )
    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))
    order: Mapped["Order"] = relationship("Order", back_populates="order_lines")
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[Decimal] = mapped_column(Numeric(10,3), nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)
    vat_rate: Mapped[Decimal] = mapped_column(Numeric(5,2), nullable=False)

    @validates("unit_price")
    def validate_price(self, key, unit_price):
        if unit_price < 0:
            raise ValueError("Incorrect value: price cannot be negative")
        return unit_price
    
    @validates("quantity")
    def validate_quantity(self, key, quantity):
        if quantity <= 0:
            raise ValueError("Incorrect value: quantity must be positive")
        return quantity
    
    @validates("vat_rate")
    def validate_vat(self, key, vat_rate: Decimal):
        if vat_rate > Decimal("1"):
            raise ValueError("VAT rate cannot exceed 1 (100%)")
        if vat_rate < Decimal("0"):
            raise ValueError("VAT rate cannot be negative")
        return vat_rate