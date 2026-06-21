from db.database import Base
from sqlalchemy import Identity, ForeignKey, String, Numeric, Integer, CheckConstraint, Enum as SQLEnum, Date, text
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from decimal import Decimal
from datetime import date
from typing import TYPE_CHECKING


from enums.order_status import OrderStatus
if TYPE_CHECKING:
    from models import OrderLine, Customer, Invoice

class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (
        CheckConstraint("order_number > 0", name="ck_positive_order_number"),
    )
    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    order_number: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    customer_id : Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)
    customer: Mapped["Customer"] = relationship("Customer", back_populates="orders")
    status: Mapped[OrderStatus] = mapped_column(SQLEnum(
                                            OrderStatus,
                                            name="order_status_enum",
                                            create_constraint=True
                                            ),
                                            nullable=False)
    order_date: Mapped[date] = mapped_column(Date, nullable=False, server_default=text("CURRENT_DATE"))
    order_lines: Mapped[list["OrderLine"]] = relationship("OrderLine", back_populates="order", cascade="all, delete-orphan")
    invoice: Mapped["Invoice"] = relationship("Invoice", back_populates="order", uselist=False)

    @validates("order_number")
    def validate_order_number(self, key, order_number):
        if order_number < 1:
            raise ValueError("Incorrect value: Order Number muste be greater or equal to 1")
        return order_number
    