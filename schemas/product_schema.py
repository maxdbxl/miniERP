from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal

class ProductResponse(BaseModel):
    id: int
    sku: str
    name: str
    description: str | None
    unit_price_ex_vat: Decimal
    vat_rate: Decimal
    category_id: int
    current_stock: Decimal

    model_config = ConfigDict(
        from_attributes=True
    )

class ProductCreate(BaseModel):
    sku: str = Field(min_length=12, 
                    max_length=12,
                    pattern=r"^[A-Z]{6}-[0-9]{5}$")
    name: str = Field(min_length=1,
                    max_length=75)
    description: str | None = None
    unit_price_ex_vat: Decimal = Field(ge=0,
                                    decimal_places=2)
    vat_rate: Decimal = Field(ge=0,
                            le=1,
                            decimal_places=2,
                            description="VAT rate between 0 and 1 (e.g. 0.21 for 21%)")
    category_id: int = Field(gt=0)
    current_stock: Decimal = Field(ge=0)

class ProductUpdate(BaseModel):
    sku: str | None = Field(
        default=None,
        min_length=12, 
        max_length=12,
        pattern=r"^[A-Z]{6}-[0-9]{5}$"
    )
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=75
    )
    description: str | None = None
    unit_price_ex_vat: Decimal | None = Field(
        default=None,
        ge=0,
        decimal_places=2
    )
    vat_rate: Decimal | None = Field(
        default=None,
        ge=0,
        le=1,
        decimal_places=2,
        description="VAT rate between 0 and 1 (e.g. 0.21 for 21%)"
    )
    category_id: int | None = Field(
        default=None,
        gt=0
    )
    current_stock: Decimal | None = Field(
        default=None,
        ge=0
    )