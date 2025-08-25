from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    category_id: int
    price: float
    description: Optional[str] = None

class ProductRead(ProductCreate):
    id: int
