from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.security import require_roles
from fastapi import Depends
from app.core.database import get_session
from app.STOCK.models.stock import Stock
from app.STOCK.models.transaction import Transaction
from app.STOCK.schemas.stock import StockAdd, StockRemove, StockRead

router = APIRouter(prefix="/stock", tags=["Stock"])

@router.post("/add", dependencies=[Depends(require_roles("Admin","StockManager"))])
def add_stock(stock_data: StockAdd, session: Session = Depends(get_session)):
    stock = session.exec(select(Stock).where(Stock.product_id == stock_data.product_id)).first()

    if not stock:
        stock = Stock(product_id=stock_data.product_id, quantity=0)
        session.add(stock)

    stock.quantity += stock_data.quantity

    transaction = Transaction(
        product_id=stock_data.product_id,
        transaction_type="purchase",
        quantity=stock_data.quantity,
        price_per_unit=stock_data.purchase_price,
        supplier=stock_data.supplier
    )
    session.add(transaction)
    session.commit()
    session.refresh(stock)

    return {
        "product_id": stock.product_id,
        "new_stock_level": stock.quantity,
        "message": "Stock updated successfully"
    }

@router.post("/remove", dependencies=[Depends(require_roles("Admin","StockManager"))])
def remove_stock(stock_data: StockRemove, session: Session = Depends(get_session)):
    stock = session.exec(select(Stock).where(Stock.product_id == stock_data.product_id)).first()

    if not stock or stock.quantity < stock_data.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    stock.quantity -= stock_data.quantity

    transaction = Transaction(
        product_id=stock_data.product_id,
        transaction_type="sale",
        quantity=stock_data.quantity,
        price_per_unit=0,  # Can be updated if sales price tracking is needed
        customer=stock_data.customer
    )
    session.add(transaction)
    session.commit()
    session.refresh(stock)

    return {
        "product_id": stock.product_id,
        "new_stock_level": stock.quantity,
        "message": "Stock reduced successfully"
    }

@router.get("/{product_id}", response_model=StockRead)
def get_stock(product_id: int, session: Session = Depends(get_session)):
    stock = session.exec(select(Stock).where(Stock.product_id == product_id)).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock
