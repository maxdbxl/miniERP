from sqlalchemy.orm import Session

from repositories.customer_repository import CustomerRepository
from schemas.customer_schema import CustomerCreate
from models import Customer

class CustomerService:

    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    def get_customer(self, session: Session, customer_id: int) -> Customer:
        customer = self.repository.get_customer_by_id(session, customer_id)
        # à remplacer par CustomerNotFoundException par la suite
        if customer is None:
            raise ValueError(f"Customer {customer_id} not found")
        return customer
    
    def add_customer(self, session: Session, data: CustomerCreate) -> Customer:
        
        return self.repository.create_customer(
            session, 
            name=data.name, 
            vat_number=data.vat_number, 
            address=data.address
            )

    

customer_service = CustomerService(CustomerRepository()) 