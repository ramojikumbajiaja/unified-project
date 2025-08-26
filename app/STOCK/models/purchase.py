from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Purchase(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    quantity: int
    price_per_unit: float
    supplier: Optional[str] = None
    date: datetime = Field(default_factory=datetime.utcnow)
