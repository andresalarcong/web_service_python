from fastapi.testclient import TestClient

class TestProductController:
    def test_create_and_get_product(self, client: TestClient):
        """
        Tests the full lifecycle: Create, Get, and verify the data.
        """
        # 1. Create a Product
        create_payload = {"name": "Test Laptop Pro", "price": 1999.99, "description": "A powerful test machine"}
        response_create = client.post("/products/", json=create_payload)

        assert response_create.status_code == 201
        created_data = response_create.json()
        assert created_data["name"] == create_payload["name"]
        assert created_data["price"] == create_payload["price"]
        assert "id" in created_data
        assert "created_at" in created_data

        product_hashid = created_data["id"]

        # 2. Get the Product by its new ID
        response_get = client.get(f"/products/{product_hashid}")
        assert response_get.status_code == 200
        get_data = response_get.json()
        assert get_data["id"] == product_hashid
        assert get_data["name"] == create_payload["name"]


    def test_get_product_not_found(self, client: TestClient):
        """
        Tests that requesting a non-existent product returns a 404 error.
        This also tests our custom exception handler.
        """
        response = client.get("/products/invalidHashId")
        assert response.status_code == 404
        assert response.json() == {"message": "Product with ID 'invalidHashId' not found."}

    def test_get_all_products(self, client: TestClient):
        """
        Tests fetching all products.
        """
        # Assuming the db is fresh or contains products from other tests
        client.post("/products/", json={"name": "Product A", "price": 10})
        client.post("/products/", json={"name": "Product B", "price": 20})

        response = client.get("/products/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 2


    def test_delete_product(self, client: TestClient):
        """
        Tests deleting a product.
        """
        # Create a product to delete
        payload = {"name": "Product to Delete", "price": 99}
        response_create = client.post("/products/", json=payload)
        product_hashid = response_create.json()["id"]

        # Delete it
        response_delete = client.delete(f"/products/{product_hashid}")
        assert response_delete.status_code == 204

        # Verify it's gone
        response_get = client.get(f"/products/{product_hashid}")
        assert response_get.status_code == 404