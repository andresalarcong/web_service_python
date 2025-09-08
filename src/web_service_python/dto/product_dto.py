from pydantic import BaseModel, Field, field_serializer, ConfigDict
from datetime import datetime

from ..app.dependencies import hashids
from ..domain.product import Product


class ProductBase(BaseModel):
    name: str = Field(..., min_length=3)
    price: float = Field(..., gt=0)
    description: str | None = None


class ProductRequestDTO(ProductBase):
    def try_parse(self) -> Product:
        return Product(name=self.name, price=self.price, description=self.description)


class ProductResponseDTO(ProductBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_serializer('id')
    def serialize_id(self, id_int: int, _info):
        return hashids.encode(id_int)