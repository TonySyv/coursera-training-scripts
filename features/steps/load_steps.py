# features/steps/load_steps.py
from behave import given
from app.models import Product
from app.database import db

@given("the following products exist")
def step_impl(context):
    for row in context.table:
        product = Product(
            id=int(row["id"]),
            name=row["name"],
            available=row["available"].lower() == "true"
        )
        db.add_product(product)
