from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Product
from decimal import Decimal

class ProductRepository:

    def create_product(self, 
                    session: Session, 
                    sku: str,
                    name: str,
                    description: str | None,
                    unit_price_ex_vat: Decimal,
                    vat_rate: Decimal,
                    category_id: int,
                    current_stock: Decimal
                    ) -> Product:
        product = Product(sku=sku,
                        name=name,
                        description=description,
                        unit_price_ex_vat=unit_price_ex_vat,
                        vat_rate=vat_rate,
                        category_id=category_id,
                        current_stock=current_stock)
        session.add(product)
        session.flush()
        return product
    
    def get_product_by_id(self, session: Session, product_id: int) -> Product | None:
        product = session.get(Product, product_id)
        return product

    def get_product_by_sku(self,
                        session: Session,
                        sku: str) -> Product | None:
        stmt = select(Product).where(Product.sku == sku)
        return session.execute(stmt).scalar_one_or_none()
    
    def get_all_products(self, session: Session) -> list[Product]:
        stmt = select(Product)
        return list(session.execute(stmt).scalars().all())

product_repository = ProductRepository()
