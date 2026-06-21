from fastapi import FastAPI

from routers.customer_router import router as customer_router
from scripts import seed

app = FastAPI()

app.include_router(
    customer_router,
    prefix="/customers",
    tags=["Customers"]
)

