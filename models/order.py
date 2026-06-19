from db.database import Base
from sqlalchemy import Identity, ForeignKey, String, Numeric, Integer, CheckConstraint, Enum as SQLEnum, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from decimal import Decimal
from datetime import date

from enums.order_status import OrderStatus
from models import OrderLine, Customer

class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (
        CheckConstraint("order_number > 0", name="ck_positive_order_number")
    )
    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    order_number: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    customer_id : Mapped[int] = mapped_column(ForeignKey("customers.id"))
    customer: Mapped["Customer"] = relationship("Customer", back_populates="orders")
    status: Mapped[OrderStatus] = mapped_column(SQLEnum(
                                            OrderStatus,
                                            name="status_enum",
                                            create_constraint=True
                                            ),
                                            nullable=False)
    order_date: Mapped[date] = mapped_column(Date, nullable=False)
    order_lines: Mapped[list["OrderLine"]] = relationship("OrderLine", back_populates="order")

    @validates("order_number")
    def validate_order_number(self, key, order_number):
        if order_number < 1:
            raise ValueError("Incorrect value: Order Number muste be greater or equal to 1")
        return order_number
    
    @validates()
    def ok():
        pass