import pytest
from fastapi.testclient import TestClient

from web_service_python.app.main import app
from web_service_python.app.dependencies import get_product_service
from web_service_python.app.dependencies import hashids
from web_service_python.repository.product_repository import ProductRepository
from web_service_python.service.product_service import ProductService


@pytest.fixture(scope="session")
def test_db_repo():
    """
    Creates a single repository instance with an in-memory SQLite database
    that persists for the entire test session.
    """
    repo = ProductRepository()
    yield repo
    repo.close_connection()


@pytest.fixture(scope="session")
def test_product_service(test_db_repo: ProductRepository):
    """
    Creates a service instance that depends on the session-scoped
    test database repository.
    """
    return ProductService(repo=test_db_repo, hashids=hashids)


@pytest.fixture(scope="session")
def client(test_product_service: ProductService):
    """
    Provides a TestClient where the get_product_service dependency
    is overridden to use our isolated test service.
    """
    # Override the real dependency with a function that returns our test service
    app.dependency_overrides[get_product_service] = lambda: test_product_service

    with TestClient(app) as test_client:
        yield test_client

    # Clean up the override after tests are done
    app.dependency_overrides.clear()