from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import date
from decimal import Decimal

from repositories.order_repository import OrderRepository
from repositories.customer_repository import CustomerRepository
from repositories.product_repository import ProductRepository
from models import Order, OrderLine, StockMovement
from enums.order_status import OrderStatus
from enums.movement_type import MovementType
from exceptions.customer_exceptions import CustomerNotFoundError
from exceptions.order_exceptions import OrderNotFoundError, InvalidOrderStatusError, InsufficientStockError
from exceptions.product_exceptions import ProductNotFoundError

class OrderService:

    def __init__(self, repository: OrderRepository, product_repository: ProductRepository, customer_repository: CustomerRepository):
        self.repository = repository
        self.product_repository = product_repository
        self.customer_repository = customer_repository

    def _generate_order_number(self, session: Session) -> str:
        #TODO: permettre encodage d'une année lors de la création de la commande ? meilleure gestion de l'année fiscale
        # éventuellement stocker year et sequence + hybrid property
        year = date.today().year

        last_order_number = (self.repository.get_last_order_number_for_year(session, year))

        if last_order_number is None:
            sequence = 1
        else:
            sequence = int(last_order_number.split("-")[-1]) + 1

        return f"{year}-{sequence:07d}"
    

    def create_order(self, session: Session, customer_id: int) -> Order:
        customer = self.customer_repository.get_customer_by_id(session, customer_id)

        if customer is None:
            raise CustomerNotFoundError()
        
        next_order_number = self._generate_order_number(session)

        order = Order(
            order_number=next_order_number,
            customer_id=customer_id,
            status=OrderStatus.DRAFT,
            order_date=date.today()
        )

        self.repository.create_order(session, order)

        return order
    
    def add_line_to_order(self, session: Session, order_id: int, product_id: int, quantity: Decimal) -> OrderLine:

        order = self.repository.get_order_by_id(session, order_id)

        if order is None:
            raise OrderNotFoundError()
        
        if order.status != OrderStatus.DRAFT:
            raise ValueError("Only draft orders can be modified")
        
        product = self.product_repository.get_product_by_id(session, product_id)

        if product is None:
            raise ProductNotFoundError()
        
        line = OrderLine(
            product_id=product.id,
            quantity=quantity,
            unit_price=product.unit_price_ex_vat,
            vat_rate= product.vat_rate
        )

        order.order_lines.append(line)

        #vérifier si flush cohérent ici
        session.flush()

        return line

    def confirm_order(self, session: Session, order_id: int):
        order = self.repository.get_order_by_id(session, order_id)

        if order is None:
            raise OrderNotFoundError()
        
        if order.status != OrderStatus.DRAFT:
            raise InvalidOrderStatusError("Only draft orders can be confirmed")
        
        if not order.order_lines:
            raise ValueError("Empty order cannot be confirmed")
        
        for line in order.order_lines:
            product = line.product
            if product.current_stock < line.quantity:
                #TODO: vérification éventuelle du délai de livraison du fournisseur + délai livraison vers client vs date de livraison souhaitée. Eventuelle possibilité de split la livraison (demande de validation au client) 
                raise InsufficientStockError(f"Insufficient stock for {product.sku}")
            
        for line in order.order_lines:
            product = line.product
            product.current_stock -= line.quantity

            movement = StockMovement(
                product_id=product.id,
                movement_type=MovementType.OUTBOUND,
                quantity=line.quantity
            )
            session.add(movement)

        order.status = OrderStatus.CONFIRMED

        session.commit()
        session.refresh(order, ["order_lines"])

        return order


order_service = OrderService(OrderRepository(), ProductRepository(), CustomerRepository())