from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.security import require_roles
from fastapi import Depends
from app.core.database import get_session
from app.STOCK.models.category import Category
from app.STOCK.schemas.category import CategoryCreate,CategoryRead

from typing import List

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=CategoryRead, dependencies=[Depends(require_roles("Admin","StockManager"))])
def create_category(category: CategoryCreate, session: Session = Depends(get_session)):
    db_category = Category(**category.dict())
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category

@router.get("/", response_model=List[CategoryRead])
def list_categories(session: Session = Depends(get_session)):
    return session.exec(select(Category)).all()
