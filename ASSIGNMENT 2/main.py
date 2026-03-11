from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()

# ---------------------------
# Sample Data
# ---------------------------
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True}
]

feedback_list = []

# ---------------------------
# Helper Function
# ---------------------------
def find_product(product_id: int):
    for p in products:
        if p["id"] == product_id:
            return p
    return None

# ---------------------------
# HOME
# ---------------------------
@app.get("/")
def home():
    return {"message": "Welcome to E-commerce API"}

# ---------------------------
# Q1 — Product Price
# ---------------------------
@app.get("/products/{product_id}/price")
def get_product_price(product_id: int):
    product = find_product(product_id)

    if not product:
        return {"error": "Product not found"}

    return {
        "name": product["name"],
        "price": product["price"]
    }

# ---------------------------
# Q2 — Filter Products
# ---------------------------
@app.get("/products/filter")
def filter_products(
        category: Optional[str] = Query(None),
        min_price: Optional[int] = Query(None),
        max_price: Optional[int] = Query(None),
        in_stock: Optional[bool] = Query(None)
):

    result = products

    if category:
        result = [p for p in result if p["category"] == category]

    if min_price is not None:
        result = [p for p in result if p["price"] >= min_price]

    if max_price is not None:
        result = [p for p in result if p["price"] <= max_price]

    if in_stock is not None:
        result = [p for p in result if p["in_stock"] == in_stock]

    return {
        "filtered_products": result,
        "count": len(result)
    }

# ---------------------------
# Q3 — Feedback API
# ---------------------------
class Feedback(BaseModel):
    customer_name: str = Field(..., min_length=2)
    product_id: int = Field(..., gt=0)
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None


@app.post("/feedback")
def submit_feedback(data: Feedback):

    feedback_list.append(data)

    return {
        "message": "Feedback submitted successfully",
        "feedback": data,
        "total_feedback": len(feedback_list)
    }

# ---------------------------
# Q4 — Products Summary
# ---------------------------
@app.get("/products/summary")
def products_summary():

    total_products = len(products)

    in_stock_count = len([p for p in products if p["in_stock"]])
    out_of_stock_count = len([p for p in products if not p["in_stock"]])

    most_expensive = max(products, key=lambda x: x["price"])
    cheapest = min(products, key=lambda x: x["price"])

    categories = list(set([p["category"] for p in products]))

    return {
        "total_products": total_products,
        "in_stock_count": in_stock_count,
        "out_of_stock_count": out_of_stock_count,
        "most_expensive": {
            "name": most_expensive["name"],
            "price": most_expensive["price"]
        },
        "cheapest": {
            "name": cheapest["name"],
            "price": cheapest["price"]
        },
        "categories": categories
    }

# ---------------------------
# Q5 — Bulk Orders
# ---------------------------
class OrderItem(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., ge=1, le=50)


class BulkOrder(BaseModel):
    company_name: str = Field(..., min_length=2)
    contact_email: str = Field(..., min_length=5)
    items: List[OrderItem]


@app.post("/orders/bulk")
def bulk_order(order: BulkOrder):

    confirmed = []
    failed = []
    grand_total = 0

    for item in order.items:

        product = find_product(item.product_id)

        if not product:
            failed.append({
                "product_id": item.product_id,
                "reason": "Product not found"
            })
            continue

        if not product["in_stock"]:
            failed.append({
                "product_id": item.product_id,
                "reason": f"{product['name']} is out of stock"
            })
            continue

        subtotal = product["price"] * item.quantity
        grand_total += subtotal

        confirmed.append({
            "product": product["name"],
            "qty": item.quantity,
            "subtotal": subtotal
        })

    return {
        "company": order.company_name,
        "confirmed": confirmed,
        "failed": failed,
        "grand_total": grand_total
    }
