from typing import List
from fastapi import APIRouter, status, Depends
from ..dto.product_dto import ProductResponseDTO, ProductRequestDTO
from ..service.product_service import ProductService
from ..app.dependencies import get_product_service

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=List[ProductResponseDTO])
def get_all(service: ProductService = Depends(get_product_service)):
    """ Get all products """
    return service.get_all_products()

@router.get("/{product_id}", response_model=ProductResponseDTO)
def get_by_id(product_id: str, service: ProductService = Depends(get_product_service)):
    """ Get product by id """
    return service.get_product_by_id(product_id)

@router.post("/", response_model=ProductResponseDTO, status_code=status.HTTP_201_CREATED)
def create(dto: ProductRequestDTO, service: ProductService = Depends(get_product_service)):
    """ Create a new product """
    return service.create_product(dto.try_parse())

@router.put("/{product_id}", response_model=ProductResponseDTO)
def update(product_id: str, dto: ProductRequestDTO, service: ProductService = Depends(get_product_service)):
    """ Update a product."""
    return service.update_product(product_id, dto.try_parse())

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(product_id: str, service: ProductService = Depends(get_product_service)):
    """ Delete a product by id """
    service.delete_product_by_id(product_id)