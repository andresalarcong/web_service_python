from fastapi import Depends, Request
from ..repository.product_repository import ProductRepository
from ..service.product_service import ProductService
from hashids import Hashids

hashids = Hashids(salt="secret", min_length=8)

product_repository_singleton = ProductRepository()

def get_product_repository(request: Request):
    return request.app.state.db_repo

def get_product_service(repo: ProductRepository = Depends(get_product_repository)):
    return ProductService(repo, hashids=hashids)