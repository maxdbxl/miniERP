from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from schemas.product_schema import ProductNested



class OrderLineResponse(BaseModel):
    id: int
    product: ProductNested
    quantity: Decimal
    unit_price: Decimal
    vat_rate: Decimal

    total_ex_vat: Decimal
    total_vat: Decimal
    total_in_vat: Decimal

    model_config = ConfigDict(from_attributes=True)

class OrderLineCreate(BaseModel):
    product: ProductNested
    quantity: Decimal
