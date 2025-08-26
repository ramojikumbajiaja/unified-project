from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.security import require_roles
from fastapi import Depends
from app.core.database import get_session
from app.STOCK.models.stock import Stock
from app.STOCK.models.product import Product
from app.STOCK.schemas.stock import StockAdd, StockRemove, StockRead

router = APIRouter(prefix="/stock", tags=["Stock"])

@router.post("/add", dependencies=[Depends(require_roles("Admin", "StockManager"))])
def add_stock(stock_data: StockAdd, session: Session = Depends(get_session)):
    product = session.exec(select(Product).where(Product.id == stock_data.product_id)).first()
    if not product:
        raise HTTPException(status_code=400, detail=f"Product with id {stock_data.product_id} does not exist")

    stock = session.exec(select(Stock).where(Stock.product_id == stock_data.product_id)).first()
    if not stock:
        stock = Stock(product_id=stock_data.product_id, quantity=0)
        session.add(stock)

    stock.quantity += stock_data.quantity

    session.commit()
    session.refresh(stock)

    return {
        "product_id": stock.product_id,
        "new_stock_level": stock.quantity,
        "message": "Stock updated successfully"
    }


@router.get("/{product_id}", response_model=StockRead)
def get_stock(product_id: int, session: Session = Depends(get_session)):
    stock = session.exec(select(Stock).where(Stock.product_id == product_id)).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock