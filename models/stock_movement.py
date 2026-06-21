from db.database import Base
from sqlalchemy import Identity, ForeignKey, String, Numeric, Integer, CheckConstraint, Enum as SQLEnum, Date, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from decimal import Decimal
from datetime import date, datetime
from typing import TYPE_CHECKING

from enums.order_status import OrderStatus
from enums.movement_type import MovementType
if TYPE_CHECKING:
    from models import OrderLine, Customer, Invoice

class StockMovement(Base):
    __tablename__ = "stock_movements"
    __table_args__ = (
        CheckConstraint("quantity > 0", name="ck_stock_movement_positive_quantity"),
    )
    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    movement_type: Mapped[MovementType] = mapped_column(SQLEnum(
                                            MovementType,
                                            name="movement_type_enum",
                                            create_constraint=True
                                            ),
                                            nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)