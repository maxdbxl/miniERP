from db.database import Base
from sqlalchemy import Identity, ForeignKey, String, Numeric, Integer, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Product

class Category(Base):
    __tablename__ = "categories"
    __table_args__ = (
        
    )
    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(75), nullable=False, unique=True)
    products: Mapped[list["Product"]] = relationship(back_populates="category")
