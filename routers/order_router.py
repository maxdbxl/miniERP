from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.session import get_session
from schemas.order_line_schema import OrderLineResponse, OrderLineCreate
from schemas.order_schema import OrderCreate, OrderResponse
from services.order_service import order_service
from exceptions.order_exceptions import OrderNotFoundError, InvalidOrderStatusError, InsufficientStockError
from exceptions.customer_exceptions import CustomerNotFoundError
from exceptions.product_exceptions import ProductNotFoundError

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderResponse, status_code=201)
def create_order(data: OrderCreate, session: Session = Depends(get_session)):
    try:
        order = order_service.create_order(session, customer_id=data.customer_id)

        session.refresh(order)
        return order
    except CustomerNotFoundError:
        raise HTTPException(status_code=404, detail="Customer not found")
    
@router.get("/", response_model=OrderResponse)
def get_order(order_id: int, session: Session = Depends(get_session)):
    try:
        order = order_service.repository.get_order_by_id(session, order_id)
        return order
    except OrderNotFoundError:
        raise HTTPException(status_code=404, detail="Order not found")
    
@router.post("/{order_id}/lines", response_model=OrderResponse)
def add_line(order_id: int,
            data: OrderLineCreate,
            session: Session = Depends(get_session)):
    
    try:
        order_service.add_line_to_order(
            session=session,
            order_id=order_id,
            product_id=data.product.id,
            quantity=data.quantity
        )
        order = order_service.repository.get_order_by_id(session, order_id)
        session.refresh(order)
        return order
    
    except OrderNotFoundError:
        raise HTTPException(status_code=404, detail="Order not found")
    
    except ProductNotFoundError:
        raise HTTPException(status_code=404, detail="Product not found")
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.post("/{order_id}/confirm", response_model=OrderResponse)
def confirm_order(order_id: int, session: Session = Depends(get_session)):
    try:
        order = order_service.confirm_order(
            session=session,
            order_id=order_id
        )

        session.refresh(order)
        return order
    
    except OrderNotFoundError:
        raise HTTPException(status_code=404, detail="Order not found")
    
    except InvalidOrderStatusError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except InsufficientStockError as e:
        raise HTTPException(status_code=409, detail=str(e))