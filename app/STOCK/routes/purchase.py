from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.STOCK.models.product import Product
from app.STOCK.models.stock import Stock
from app.STOCK.models.transaction import Transaction
from app.STOCK.models.purchase import Purchase
from app.core.database import get_session
from app.core.security import require_roles
from app.STOCK.schemas.purchase import PurchaseCreate, PurchaseRead

router = APIRouter(prefix="/purchase", tags=["Purchases"])

@router.post("/create", response_model=PurchaseRead, dependencies=[Depends(require_roles("Admin", "StockManager"))])
def create_purchase(purchase_data: PurchaseCreate, session: Session = Depends(get_session)):
    product = session.exec(select(Product).where(Product.id == purchase_data.product_id)).first()
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with id {purchase_data.product_id} does not exist")

    stock = session.exec(select(Stock).where(Stock.product_id == purchase_data.product_id)).first()
    if not stock or stock.quantity < purchase_data.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock for this purchase")
    stock.quantity -= purchase_data.quantity

    purchase = Purchase(
        product_id=purchase_data.product_id,
        quantity=purchase_data.quantity,
        price_per_unit=purchase_data.purchase_price,
        supplier=purchase_data.supplier
    )
    session.add(purchase)

    transaction = Transaction(
        product_id=purchase_data.product_id,
        transaction_type="purchase",
        quantity=purchase_data.quantity,
        price_per_unit=purchase_data.purchase_price,
        supplier=purchase_data.supplier
    )
    session.add(transaction)

    session.commit()
    session.refresh(purchase)
    session.refresh(stock)
    return PurchaseRead.from_orm(purchase)