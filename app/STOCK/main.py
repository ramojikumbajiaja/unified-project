from fastapi import FastAPI
from app.core.database import init_db as create_db_and_tables
from app.STOCK.routes.product_routes import router as product_router
from app.STOCK.routes.category_routes import router as category_router
from app.STOCK.routes.stock_routes import router as stock_router
from app.STOCK.routes.transaction_routes import router as transaction_router

app = FastAPI(title="Stock Flow API - SQLModel + Postgres")

app.include_router(product_router)
app.include_router(category_router)
app.include_router(stock_router)
app.include_router(transaction_router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def root():
    return {"message": "Welcome to the Stock Flow API"}
