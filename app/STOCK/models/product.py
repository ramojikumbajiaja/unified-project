from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from .category import Category

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    category_id: int = Field(foreign_key="category.id")
    price: float
    description: Optional[str] = None

    category: Optional[Category] = Relationship()
