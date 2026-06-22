from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Order, OrderLine
from decimal import Decimal

class OrderRepository:
    def create_order(self, session: Session, order: Order):
        session.add(order)
        session.flush()
        return order

    def get_order_by_id(self, session: Session, order_id: int) -> Order | None:
        order = session.get(Order, order_id)
        return order
    # vérifier doc SQLAlchemy comment proprement gérer l'ajout de lignes (via append dans le service ou via le repository)
    # def add_order_line(self, session: Session, line: OrderLine) -> OrderLine:
    #     session.add(line)
    #     session.flush()
    #     return line

    def get_order_with_lines(self, session: Session, order_id: int) -> Order | None:
        stmt = select(Order).where(Order.id == order_id)
        return session.execute(stmt).scalar_one_or_none()
    
    def get_last_order_number_for_year(self, session: Session, year: int) -> str | None:
        stmt = select(Order.order_number).where(Order.order_number.like(f"{year}-%")).order_by(Order.order_number.desc()).limit(1)

        return session.execute(stmt).scalar_one_or_none()
    
order_repository = OrderRepository()