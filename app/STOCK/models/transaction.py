from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from .product import Product

class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    transaction_type: str  # "purchase" or "sale"
    quantity: int
    price_per_unit: float
    supplier: Optional[str] = None
    customer: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    product: Optional[Product] = Relationship()
