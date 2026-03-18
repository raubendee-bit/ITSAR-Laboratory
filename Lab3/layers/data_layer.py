# ============================================================
# DATA LAYER — layers/data_layer.py
# Responsible for storing and retrieving product data.
# No business rules live here. This layer only reads/writes.
# ============================================================

# In-memory product "database"
_products = {
    "P001": {"id": "P001", "name": "Laptop",       "price": 49999.00, "stock": 5},
    "P002": {"id": "P002", "name": "Mechanical Keyboard", "price": 3499.00,  "stock": 10},
    "P003": {"id": "P003", "name": "USB-C Hub",    "price": 1299.00,  "stock": 0},
    "P004": {"id": "P004", "name": "Monitor",      "price": 15999.00, "stock": 3},
    "P005": {"id": "P005", "name": "Webcam",       "price": 2799.00,  "stock": 7},
}


def get_all_products():
    """Return a copy of all products."""
    return list(_products.values())


def get_product_by_id(product_id: str):
    """Return a single product dict, or None if not found."""
    return _products.get(product_id)


def reduce_stock(product_id: str, quantity: int):
    """
    Deduct quantity from a product's stock.
    Assumes business logic has already validated this is safe.
    """
    _products[product_id]["stock"] -= quantity
    return _products[product_id]
