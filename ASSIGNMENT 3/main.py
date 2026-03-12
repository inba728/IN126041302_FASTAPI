from fastapi import FastAPI, HTTPException

app = FastAPI()

# -------------------------
# Sample Data
# -------------------------

products = [
    {"id": 1, "name": "Laptop", "price": 499, "stock": 10, "category": "Electronics"},
    {"id": 2, "name": "Keyboard", "price": 99, "stock": 15, "category": "Electronics"},
    {"id": 3, "name": "Mouse", "price": 49, "stock": 20, "category": "Electronics"},
    {"id": 4, "name": "USB Hub", "price": 799, "stock": 0, "category": "Electronics"}
]

orders = [
    {"id": 1, "product_id": 1, "quantity": 2},
    {"id": 2, "product_id": 3, "quantity": 1}
]

# -------------------------
# Home
# -------------------------

@app.get("/")
def home():
    return {"message": "Welcome to Product Inventory API"}

# -------------------------
# Get All Products
# -------------------------

@app.get("/products")
def get_products():
    return products

# -------------------------
# Add Product
# -------------------------

@app.post("/products")
def add_product(product: dict):
    products.append(product)
    return {"message": "Product added", "product": product}

# -------------------------
# Filter Products
# -------------------------

@app.get("/products/filter")
def filter_products(min_price: int = 0):
    filtered = [p for p in products if p["price"] >= min_price]
    return filtered

# -------------------------
# Compare Products
# -------------------------

@app.get("/products/compare")
def compare_products(id1: int, id2: int):

    product1 = next((p for p in products if p["id"] == id1), None)
    product2 = next((p for p in products if p["id"] == id2), None)

    if not product1 or not product2:
        raise HTTPException(status_code=404, detail="Product not found")

    return {
        "product1": product1,
        "product2": product2,
        "price_difference": abs(product1["price"] - product2["price"])
    }

# -------------------------
# Inventory Audit (TASK)
# -------------------------

@app.get("/products/audit")
def products_audit():

    total_products = len(products)

    in_stock_products = [p for p in products if p["stock"] > 0]
    in_stock_count = len(in_stock_products)

    out_of_stock_names = [p["name"] for p in products if p["stock"] == 0]

    total_stock_value = sum(p["price"] * 10 for p in in_stock_products)

    most_expensive = max(products, key=lambda p: p["price"])

    return {
        "total_products": total_products,
        "in_stock_count": in_stock_count,
        "out_of_stock_names": out_of_stock_names,
        "total_stock_value": total_stock_value,
        "most_expensive": {
            "name": most_expensive["name"],
            "price": most_expensive["price"]
        }
    }

# -------------------------
# BONUS: Apply Discount
# -------------------------

@app.put("/products/discount")
def apply_discount(category: str, discount_percent: int):

    updated_products = []

    for product in products:
        if product["category"].lower() == category.lower():
            new_price = int(product["price"] * (1 - discount_percent / 100))
            product["price"] = new_price
            updated_products.append(product)

    if len(updated_products) == 0:
        return {"message": "No products found in this category"}

    return {
        "updated_count": len(updated_products),
        "products": updated_products
    }

# -------------------------
# Update Product
# -------------------------

@app.put("/products/{product_id}")
def update_product(product_id: int, updated_product: dict):

    for index, product in enumerate(products):
        if product["id"] == product_id:
            products[index] = updated_product
            return {"message": "Product updated", "product": updated_product}

    raise HTTPException(status_code=404, detail="Product not found")

# -------------------------
# Delete Product
# -------------------------

@app.delete("/products/{product_id}")
def delete_product(product_id: int):

    for product in products:
        if product["id"] == product_id:
            products.remove(product)
            return {"message": "Product deleted"}

    raise HTTPException(status_code=404, detail="Product not found")

# -------------------------
# Get Single Product
# -------------------------

@app.get("/products/{product_id}")
def get_product(product_id: int):

    for product in products:
        if product["id"] == product_id:
            return product

    raise HTTPException(status_code=404, detail="Product not found")

# -------------------------
# Orders
# -------------------------

@app.get("/orders")
def get_orders():
    return orders
