from pydantic import BaseModel
from typing import Optional

class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryRead(CategoryCreate):
    id: int
