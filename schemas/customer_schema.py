from pydantic import BaseModel, ConfigDict, Field

class CustomerResponse(BaseModel):
    id: int
    name: str
    vat_number: str
    address: str | None
    customer_number: str

    #pour hybrid-property customer_number
    model_config = ConfigDict(
        from_attributes=True
    )

class CustomerCreate(BaseModel):
    name: str
    vat_number: str = Field(min_length=8)
    address: str | None = None