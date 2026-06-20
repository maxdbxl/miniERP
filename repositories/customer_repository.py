from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Customer

class CustomerRepository:

    def create_customer(self, session: Session, name: str, vat_number: str, address: str | None):
        customer = Customer(name=name, vat_number=vat_number, address=address)
        session.add(customer)
        session.flush()
        return customer

    def get_customer_by_id(self, session: Session, customer_id: int) -> Customer | None:
        customer = session.get(Customer, customer_id)
        return customer 

    def get_customer_by_number(self, session: Session, customer_number: str) -> Customer | None:
        customer = session.get(Customer, customer_number)
        return customer
    
customer_repository = CustomerRepository()

