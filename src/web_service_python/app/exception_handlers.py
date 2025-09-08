from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .exceptions import (
    ProductNotFoundException,
    ProductAlreadyExistsException,
    InvalidBusinessRuleException,
    InvalidProductDataException,
)

def add_exception_handlers(app: FastAPI):
    """
    Registers custom exception handlers with the FastAPI application.
    This allows the application to return specific HTTP status codes and error
    messages for different types of business logic failures.
    """

    @app.exception_handler(ProductNotFoundException)
    async def product_not_found_handler(_: Request, exc: ProductNotFoundException):
        """
        Handles the case where a product is not found and returns a 404 error.
        """
        return JSONResponse(
            status_code=404,
            content={"message": str(exc)}
        )

    @app.exception_handler(ProductAlreadyExistsException)
    async def product_already_exists_handler(_: Request, exc: ProductAlreadyExistsException):
        """
        Handles the case where a product being created already exists, returning a 409 error.
        """
        return JSONResponse(
            status_code=409,  # 409 Conflict
            content={"message": str(exc)}
        )

    @app.exception_handler(InvalidBusinessRuleException)
    async def invalid_business_rule_handler(_: Request, exc: InvalidBusinessRuleException):
        """
        Handles generic business rule violations, returning a 422 error.
        """
        return JSONResponse(
            status_code=422,  # 422 Unprocessable Entity
            content={"message": str(exc)}
        )

    @app.exception_handler(InvalidProductDataException)
    async def invalid_product_data_handler(_: Request, exc: InvalidProductDataException):
        """
        Handles errors related to invalid input data from the client, returning a 400 error.
        """
        return JSONResponse(
            status_code=400,  # 400 Bad Request
            content={"message": str(exc)}
        )