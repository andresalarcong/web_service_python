from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Product(BaseModel):
    id: Optional[int] = None
    name: str
    price: float
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None