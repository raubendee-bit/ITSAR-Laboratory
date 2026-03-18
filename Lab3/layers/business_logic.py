from layers import data_layer


class BusinessRuleViolation(Exception):
    """
    Raised when an order request breaks a business rule.
    Carries a human-readable message and an HTTP status code.
    """
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


# ------------------------------------------------------------------
# Rule 1 — Product must exist
# ------------------------------------------------------------------
def _rule_product_exists(product_id: str):
    product = data_layer.get_product_by_id(product_id)
    if product is None:
        raise BusinessRuleViolation(
            f"Product with ID '{product_id}' does not exist.",
            status_code=404
        )
    return product


# ------------------------------------------------------------------
# Rule 2 — Quantity must be a positive integer (≥ 1)
# ------------------------------------------------------------------
def _rule_valid_quantity(quantity):
    try:
        quantity = int(quantity)
    except (ValueError, TypeError):
        raise BusinessRuleViolation("Quantity must be a whole number.")

    if quantity <= 0:
        raise BusinessRuleViolation(
            "Quantity must be greater than zero. "
            "You cannot order zero or negative items."
        )
    return quantity


# ------------------------------------------------------------------
# Rule 3 — Product must have enough stock
# ------------------------------------------------------------------
def _rule_sufficient_stock(product: dict, quantity: int):
    if product["stock"] == 0:
        raise BusinessRuleViolation(
            f"'{product['name']}' is currently out of stock.",
            status_code=409
        )
    if quantity > product["stock"]:
        raise BusinessRuleViolation(
            f"Insufficient stock for '{product['name']}'. "
            f"Requested: {quantity}, Available: {product['stock']}.",
            status_code=409
        )


# ------------------------------------------------------------------
# Public service functions (called by the presentation layer)
# ------------------------------------------------------------------

def get_products():
    """Return all products from the data layer."""
    return data_layer.get_all_products()


def get_product(product_id: str):
    """Return a single product, raising an error if it doesn't exist."""
    return _rule_product_exists(product_id)


def place_order(product_id: str, quantity):
    """
    Orchestrates all business rule checks for an order, then
    commits the stock deduction if every rule passes.

    Returns a result dict on success.
    Raises BusinessRuleViolation on any rule failure.
    """
    # Apply rules in sequence — each raises on failure
    product  = _rule_product_exists(product_id)
    quantity = _rule_valid_quantity(quantity)
    _rule_sufficient_stock(product, quantity)

    # All rules passed — commit to the data layer
    updated = data_layer.reduce_stock(product_id, quantity)

    return {
        "message":        "Order successful",
        "product":        updated["name"],
        "orderedQty":     quantity,
        "remainingStock": updated["stock"],
        "unitPrice":      updated["price"],
        "totalCost":      round(updated["price"] * quantity, 2),
    }
