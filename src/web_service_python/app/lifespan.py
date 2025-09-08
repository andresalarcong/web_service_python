from contextlib import asynccontextmanager
from fastapi import FastAPI
from ..repository.product_repository import ProductRepository


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db_repo = ProductRepository()
    yield
    app.state.db_repo.close_connection()