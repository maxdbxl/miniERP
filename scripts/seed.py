
from decimal import Decimal

from sqlalchemy import select

from db.session import SessionLocal
from models import Category, Customer, Product

def seed_categories(session):
    categories = [
    Category(name="Electronics"),
    Category(name="Office"),
    Category(name="Furniture"),
    ]

    for category in categories:
        exists = session.scalar(
            select(Category).where(
                Category.name == category.name
            )
        )

        if not exists:
            session.add(category)

def seed_customers(session):
    customers = [
    Customer(
    name="ACME Corporation",
    vat_number="BE0123456789",
    address="Rue de la Loi 16, Bruxelles",
    ),
    Customer(
    name="Globex",
    vat_number="BE9876543210",
    address="Place Saint-Lambert 10, Liège",
    ),
    Customer(
    name="Initech",
    vat_number="BE0456123789",
    address="Avenue Louise 250, Bruxelles",
    ),
    Customer(
    name="Umbrella",
    vat_number="BE0789456123",
    address="Chaussée de Charleroi 50, Namur",
    ),
    Customer(
    name="Wayne Enterprises",
    vat_number="BE0234567891",
    address="Grand Place 1, Mons",
    ),
    ]

    for customer in customers:
        exists = session.scalar(
            select(Customer).where(
                Customer.vat_number == customer.vat_number
            )
        )

        if not exists:
            session.add(customer)

def seed():
    with SessionLocal() as session:

        seed_categories(session)
        session.flush()

        seed_customers(session)

        session.commit()

        print("Database seeded successfully")


if __name__ == "__main__":
    seed()
