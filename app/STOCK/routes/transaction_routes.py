from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.core.security import require_roles
from fastapi import Depends
from app.core.database import get_session
from app.STOCK.models.transaction import Transaction
from app.STOCK.schemas.transaction import TransactionRead
from typing import List, Optional

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.get("/", response_model=List[TransactionRead])
def get_transactions(type: Optional[str] = None, session: Session = Depends(get_session)):
    stmt = select(Transaction)
    if type:
        stmt = stmt.where(Transaction.transaction_type == type)
    return session.exec(stmt).all()
