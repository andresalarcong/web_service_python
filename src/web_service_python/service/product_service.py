import uuid
from hashids import Hashids
from datetime import datetime, timezone
from ..domain.product import Product
from ..repository.product_repository import ProductRepository
from ..app.exceptions import (
    ProductNotFoundException,
)


class ProductService:
    def __init__(self, repo: ProductRepository, hashids: Hashids):
        self.repo = repo
        self.hashids = hashids

    def get_all_products(self) -> list[Product]:
        return self.repo.find_all()

    def get_product_by_id(self, hash_id: str) -> Product:
        decoded_ids = self.hashids.decode(hash_id)
        if not decoded_ids:
            raise ProductNotFoundException(f"Product with ID '{hash_id}' not found.")
        product_id = decoded_ids[0]

        product = self.repo.find_by_id(product_id)
        if product is None:
            raise ProductNotFoundException(f"Product with ID '{hash_id}' not found.")
        return product

    def create_product(self, product: Product) -> Product:
        product.created_at = datetime.now(timezone.utc)
        product.updated_at = datetime.now(timezone.utc)

        return self.repo.create(product)

    def update_product(self, product_id: str, product: Product) -> Product:
        product_to_update = self.get_product_by_id(product_id)

        product_to_update.name = product.name
        product_to_update.price = product.price
        product_to_update.description = product.description
        product_to_update.updated_at = datetime.utcnow()

        return self.repo.update(product_to_update)

    def delete_product_by_id(self, product_id: str) -> None:
        product_to_delete = self.get_product_by_id(product_id)
        self.repo.delete(product_to_delete.id)