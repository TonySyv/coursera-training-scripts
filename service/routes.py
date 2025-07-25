# service/routes.py
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.models import Product
from app.database import db

router = APIRouter()

# Task 4a: READ
@router.get("/products/{product_id}", response_model=Product)
def read_product(product_id: int):
    product = db.read_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Task 4b: UPDATE
@router.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, name: str):
    updated = db.update_product_name(product_id, name)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated

# Task 4c: DELETE
@router.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int):
    success = db.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")

# Task 4d: LIST ALL / BY NAME / BY CATEGORY / BY AVAILABILITY
@router.get("/products", response_model=List[Product])
def list_products(
    name: Optional[str] = None,
    category: Optional[str] = None,
    available: Optional[bool] = None,
):
    if name:
        return db.find_by_name(name)
    if category:
        return db.find_by_category(category)
    if available is not None:
        return db.find_by_availability(available)
    return db.list_all_products()
