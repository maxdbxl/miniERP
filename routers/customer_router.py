from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from schemas.customer_schema import CustomerResponse, CustomerCreate
from exceptions.customer_exceptions import CustomerNotFoundError, WrongVATNumberError, CustomerAlreadyExistsError
from services.customer_service import customer_service
from db.session import get_session

router = APIRouter()

@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, session: Session = Depends(get_session)):
    try:
        return customer_service.get_customer(session=session, customer_id=customer_id)
    except CustomerNotFoundError:
        raise HTTPException(status_code=404, detail="Customer not found")


@router.post("/", response_model=CustomerResponse, status_code=201)
def create_customer(data: CustomerCreate, session: Session = Depends(get_session)):
    try:
        customer = customer_service.add_customer(session=session, data=data)
        return customer
    except CustomerAlreadyExistsError:
        raise HTTPException(
            status_code=409,
            detail="Customer already exists"
        )


