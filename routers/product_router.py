from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.session import get_session
from schemas.product_schema import ProductCreate, ProductResponse
from services.product_service import product_service
from exceptions.product_exceptions import ProductNotFoundError, ProductAlreadyExistsError

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=list[ProductResponse])
def get_all_products(session: Session = Depends(get_session)):
    return product_service.get_all_products(session)

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, session: Session = Depends(get_session)):
    try:
        return product_service.get_product(session, product_id)
    except ProductNotFoundError:
        raise HTTPException(status_code=404,
                            detail="Product not found")
    
@router.post("/", response_model=ProductCreate, status_code=201)
def create_product(data: ProductCreate, session: Session = Depends(get_session)):
    try:
        product = product_service.add_product(session, data)
        return product
    except ProductAlreadyExistsError:
        raise HTTPException(
            status_code=409,
            detail="Product already exists"
        )