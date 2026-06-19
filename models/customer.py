from db.database import Base
from sqlalchemy import Identity, ForeignKey, String, Numeric, Integer, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from models import Order

class Customer(Base):
    __tablename__ = "customers"
    __table_args__ = (
        
    )
    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(75), nullable=False)
    orders: Mapped[list["Order"]] = relationship(back_populates="customer")
