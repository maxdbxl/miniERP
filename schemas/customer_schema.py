from pydantic import BaseModel, ConfigDict

class CustomerResponse(BaseModel):
    id: int
    name: str
    vat_number: str
    address: str
    customer_number: str

    #pour hybrid-property customer_number
    model_config = ConfigDict(
        from_attributes=True
    )

class CustomerCreate(BaseModel):
    name: str
    vat_number: str
    address: str | None = None