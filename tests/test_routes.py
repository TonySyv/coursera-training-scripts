# tests/test_routes.py
import json
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Task 3a: READ test case
def test_read_product_by_id():
    response = client.get("/products/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

# Task 3b: UPDATE test case
def test_update_product_name():
    payload = {"name": "Updated Sundae"}
    response = client.put("/products/1", data=json.dumps(payload))
    assert response.status_code == 200
    updated = response.json()
    assert updated["name"] == "Updated Sundae"

# Task 3c: DELETE test case
def test_delete_product():
    response = client.delete("/products/2")
    assert response.status_code == 204
    confirm = client.get("/products/2")
    assert confirm.status_code == 404

# Task 3d: LIST ALL test case
def test_list_all_products():
    response = client.get("/products")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

# Task 3e: LIST BY NAME test case
def test_list_products_by_name():
    response = client.get("/products?name=Sundae")
    assert response.status_code == 200
    for product in response.json():
        assert "Sundae" in product["name"]

# Task 3f: LIST BY CATEGORY test case
def test_list_products_by_category():
    response = client.get("/products?category=Dessert")
    assert response.status_code == 200
    for product in response.json():
        assert product["category"] == "Dessert"

# Task 3g: LIST BY AVAILABILITY test case
def test_list_products_by_availability():
    response = client.get("/products?available=true")
    assert response.status_code == 200
    for product in response.json():
        assert product["available"] is True
