from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from datetime import date
from enums.order_status import OrderStatus
from schemas.order_line_schema import OrderLineResponse



class OrderResponse(BaseModel):
    id: int
    order_number: str
    customer_id: int
    status: OrderStatus
    order_date: date

    order_lines: list[OrderLineResponse]

    total_ex_vat: Decimal
    total_vat: Decimal
    total_inc_vat: Decimal

    model_config = ConfigDict(from_attributes=True)

class OrderCreate(BaseModel):
    customer_id: int

