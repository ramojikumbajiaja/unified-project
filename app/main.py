from fastapi import FastAPI
from app.core.database import init_db
from app.IAM.router import router as iam_router
from app.HRM.router import router as hrm_router
from app.STOCK.routes.category_routes import router as stock_categories
from app.STOCK.routes.product_routes import router as stock_products
from app.STOCK.routes.stock_routes import router as stock_stock
from app.STOCK.routes.transaction_routes import router as stock_transactions


app = FastAPI(title="Unified App")

@app.on_event("startup")

def startup():
    init_db()

app.include_router(iam_router, prefix="/iam", tags=["IAM"])
app.include_router(hrm_router, tags=["HRM"])
# STOCK endpoints
app.include_router(stock_categories, prefix="/stock")
app.include_router(stock_products, prefix="/stock")
app.include_router(stock_stock, prefix="/stock")
app.include_router(stock_transactions, prefix="/stock")


@app.get("/")
def root():
    return {"message": "Unified App Running"}
