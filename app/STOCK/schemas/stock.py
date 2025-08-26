from pydantic import BaseModel,Field
from typing import Optional

class StockAdd(BaseModel):
    product_id: int
    quantity: int
    purchase_price: float
    supplier: str

class StockRemove(BaseModel):
    product_id: int
    quantity: int
    customer: str

class StockRead(BaseModel):
    product_id: int
    quantity: int
    