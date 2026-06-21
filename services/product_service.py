from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from repositories.product_repository import ProductRepository
from schemas.product_schema import ProductCreate
from models import Product
from exceptions.product_exceptions import ProductAlreadyExistsError, ProductNotFoundError

class ProductService:

    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def get_product(self, session: Session, product_id: int) -> Product:
        product = self.repository.get_product_by_id(session, product_id)
        if product is None:
            raise ProductNotFoundError(f"Product {product_id} not found")
        return product
    
    def get_product_by_sku(self, session: Session, sku: str) -> Product:
        product = self.repository.get_product_by_sku(session, sku)
        if product is None:
            raise ProductNotFoundError(f"Product SKU{sku} not found")
        return product
    
    def get_all_products(self, session: Session) -> list[Product]:
        products = self.repository.get_all_products(session)
        return products
    
    def add_product(self, session: Session, data: ProductCreate) -> Product:

        try:
            product = self.repository.create_product(
                session,
                sku=data.sku,
                name=data.name,
                description=data.description,
                unit_price_ex_vat=data.unit_price_ex_vat,
                vat_rate=data.vat_rate,
                category_id=data.category_id,
                current_stock=data.current_stock,
            )
            session.commit()
            session.refresh(product)
            return product
        
        except IntegrityError as e:
            session.rollback()
            #TODO: ajouter UQ constraint on model & alembic + check if in str(e.orig)
            raise ProductAlreadyExistsError(f"Product with SKU  {data.sku} already exists")
        
product_service = ProductService(ProductRepository())