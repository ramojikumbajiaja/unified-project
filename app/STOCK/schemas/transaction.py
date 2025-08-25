from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TransactionCreate(BaseModel):
    product_id: int
    transaction_type: str  # "purchase" or "sale"
    quantity: int
    price_per_unit: float
    supplier: Optional[str] = None
    customer: Optional[str] = None

class TransactionRead(TransactionCreate):
    id: int
    created_at: datetime
