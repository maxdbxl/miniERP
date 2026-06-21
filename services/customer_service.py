from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from repositories.customer_repository import CustomerRepository
from schemas.customer_schema import CustomerCreate
from models import Customer
from exceptions.customer_exceptions import CustomerAlreadyExistsError, CustomerNotFoundError

class CustomerService:

    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    def get_customer(self, session: Session, customer_id: int) -> Customer:
        customer = self.repository.get_customer_by_id(session, customer_id)
        # à remplacer par CustomerNotFoundException par la suite
        if customer is None:
            raise CustomerNotFoundError()
        return customer
    
    def add_customer(self, session: Session, data: CustomerCreate) -> Customer:
        try:
            customer = self.repository.create_customer(
                session, 
                name=data.name, 
                vat_number=data.vat_number, 
                address=data.address
                )
            session.commit()
            session.refresh(customer)
        except IntegrityError as e:
            session.rollback()

            if "uq_customers_vat_number" in str(e.orig):
                raise CustomerAlreadyExistsError()
            raise
        return customer

    

customer_service = CustomerService(CustomerRepository()) 