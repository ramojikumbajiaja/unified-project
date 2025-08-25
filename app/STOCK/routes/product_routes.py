from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.security import require_roles
from fastapi import Depends
from app.core.database import get_session
from app.STOCK.models.product import Product
from app.STOCK.schemas.product import ProductCreate, ProductRead
from typing import List

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductRead, dependencies=[Depends(require_roles("Admin","StockManager"))])
def create_product(product: ProductCreate, session: Session = Depends(get_session)):
    db_product = Product(**product.dict())
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

@router.get("/", response_model=List[ProductRead])
def list_products(session: Session = Depends(get_session)):
    return session.exec(select(Product)).all()

@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductRead, dependencies=[Depends(require_roles("Admin","StockManager"))])
def update_product(product_id: int, product_data: ProductCreate, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for key, value in product_data.dict().items():
        setattr(product, key, value)
    
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

@router.delete("/{product_id}", dependencies=[Depends(require_roles("Admin","StockManager"))])
def delete_product(product_id: int, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    session.delete(product)
    session.commit()
    return {"message": "Product deleted successfully"}
