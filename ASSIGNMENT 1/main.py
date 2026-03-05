from fastapi import FastAPI

app = FastAPI()

# Sample Data
products = [
    {"id": 1, "name": "Wireless Mouse", "category": "Electronics", "price": 599, "in_stock": True},
    {"id": 2, "name": "Mechanical Keyboard", "category": "Electronics", "price": 2499, "in_stock": True},
    {"id": 3, "name": "USB Cable", "category": "Electronics", "price": 199, "in_stock": False},
    {"id": 4, "name": "Notebook", "category": "Stationery", "price": 99, "in_stock": True},
    {"id": 5, "name": "Pen Set", "category": "Stationery", "price": 49, "in_stock": True},
    {"id": 6, "name": "Desk Lamp", "category": "Electronics", "price": 899, "in_stock": False},
    {"id": 7, "name": "Highlighter Pack", "category": "Stationery", "price": 149, "in_stock": True},
]

@app.get("/")
def home():
    return {"message": "Welcome to My E-commerce Store API"}

# 1️⃣ Filter by Category
@app.get("/products/category/{category_name}")
def get_by_category(category_name: str):
    result = [p for p in products if p["category"].lower() == category_name.lower()]
    if not result:
        return {"error": "No products found in this category"}
    return {"category": category_name, "products": result, "total": len(result)}

# 2️⃣ In-Stock Products
@app.get("/products/instock")
def get_instock():
    available = [p for p in products if p["in_stock"] == True]
    return {"in_stock_products": available, "count": len(available)}

# 3️⃣ Store Summary
@app.get("/store/summary")
def store_summary():
    in_stock_count = len([p for p in products if p["in_stock"]])
    out_stock_count = len(products) - in_stock_count
    categories = list(set([p["category"] for p in products]))

    return {
        "store_name": "My E-commerce Store",
        "total_products": len(products),
        "in_stock": in_stock_count,
        "out_of_stock": out_stock_count,
        "categories": categories,
    }

# 4️⃣ Search Products
@app.get("/products/search/{keyword}")
def search_products(keyword: str):
    results = [
        p for p in products
        if keyword.lower() in p["name"].lower()
    ]
    if not results:
        return {"message": "No products matched your search"}
    return {"keyword": keyword, "results": results, "total_matches": len(results)}

# 5️⃣ Best Deal & Premium Pick
@app.get("/products/deals")
def get_deals():
    cheapest = min(products, key=lambda p: p["price"])
    expensive = max(products, key=lambda p: p["price"])

    return {
        "best_deal": cheapest,
        "premium_pick": expensive,
    }
