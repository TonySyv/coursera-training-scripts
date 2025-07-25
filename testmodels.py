# tests/test_models.py

def test_read_product_by_id():
    product = Product(id=1, name="Sundae", available=True)
    retrieved = db.read_product(product.id)
    assert retrieved.name == product.name
    assert retrieved.available == True

def test_update_product_name():
    product = Product(id=2, name="Burger", available=True)
    db.update_product_name(product.id, "Cheeseburger")
    updated = db.read_product(product.id)
    assert updated.name == "Cheeseburger"

def test_delete_product():
    product = Product(id=3, name="Fries", available=True)
    db.delete_product(product.id)
    deleted = db.read_product(product.id)
    assert deleted is None

def test_list_all_products():
    products = db.list_all_products()
    assert isinstance(products, list)
    assert all(isinstance(p, Product) for p in products)

def test_find_product_by_name():
    db.add_product(Product(id=4, name="Pie", available=True))
    result = db.find_by_name("Pie")
    assert result.name == "Pie"

def test_find_products_by_availability():
    # Setup
    db.add_product(Product(id=5, name="Taco", available=True))
    db.add_product(Product(id=6, name="Pasta", available=False))
    db.add_product(Product(id=7, name="Salad", available=True))

    # Action
    available_products = db.find_by_availability(True)

    # Assert
    assert all(p.available for p in available_products)
    assert set(p.name for p in available_products) == {"Taco", "Salad"}
