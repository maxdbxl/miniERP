from db.database import Base
from sqlalchemy import Identity, ForeignKey, String, Numeric, Integer, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from decimal import Decimal
import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Category
class Product(Base):
    __tablename__ = "products"
    __table_args__ = (
        CheckConstraint("unit_price_ex_vat >= 0", name="ck_positive_price"),
        CheckConstraint("vat_rate >= 0 AND vat_rate <= 1", name="ck_product_vat_rate"),
        CheckConstraint("sku ~ '^[A-Z]{6}-[0-9]{5}$'", name="ck_valid_sku"),
        CheckConstraint("current_stock >= 0", name="ck_non_negative_stock"),
    )
    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    sku: Mapped[str] = mapped_column(String(12), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(75), nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    unit_price_ex_vat: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)
    vat_rate: Mapped[Decimal] = mapped_column(Numeric(5,2), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    category: Mapped["Category"] = relationship("Category", back_populates="products")
    current_stock: Mapped[Decimal] = mapped_column(Numeric(10,3), nullable=False)

    @validates("unit_price_ex_vat")
    def validate_price(self, key, unit_price_ex_vat):
        if unit_price_ex_vat < 0:
            raise ValueError("Incorrect value: price cannot be negative")
        return unit_price_ex_vat
    
    @validates("vat_rate")
    def validate_vat(self, key, vat_rate: Decimal):
        if vat_rate > Decimal("1"):
            raise ValueError("VAT rate cannot exceed 1 (100%)")
        if vat_rate < Decimal("0"):
            raise ValueError("VAT rate cannot be negative")
        return vat_rate

    @validates("sku")
    def validate_sku(self, key, sku: str):
        pattern = r"^[A-Z]{6}-[0-9]{5}$"
        match = re.fullmatch(pattern, sku)
        if not match:
            raise ValueError("Invalid SKU format")
        return sku
    
    @validates("current_stock")
    def validate_current_stock(self, key, current_stock: Decimal):
        if current_stock < 0:
            raise ValueError("Incorrect value: stock cannot be negative")
        return current_stock