from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from .product import Product

class Stock(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id", unique=True)
    quantity: int = Field(default=0)

    product: Optional[Product] = Relationship()
