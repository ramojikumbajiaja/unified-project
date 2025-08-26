from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PurchaseCreate(BaseModel):
    product_id: int = Field(..., description="ID of the product being purchased")
    quantity: int = Field(..., gt=0, description="Quantity to purchase")
    purchase_price: float = Field(..., gt=0, description="Price per unit")
    supplier: Optional[str] = Field(None, description="Supplier name")

class PurchaseRead(BaseModel):
    id: int
    product_id: int
    quantity: int
    price_per_unit: float
    supplier: Optional[str] = None
    date: datetime

    class Config:
        from_attributes = True
