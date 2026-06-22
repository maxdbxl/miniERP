from fastapi import FastAPI

from routers.customer_router import router as customer_router
from routers.order_router import router as order_router
from routers.product_router import router as product_router
from scripts import seed

app = FastAPI()

app.include_router(
    customer_router,
    prefix="/customers",
    tags=["Customers"]
)
app.include_router(order_router)
app.include_router(product_router)

