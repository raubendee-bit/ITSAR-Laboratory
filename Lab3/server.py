# ============================================================
# PRESENTATION LAYER — server.py
# Handles HTTP routing only. No business rules live here.
# All decisions are delegated to the business logic layer.
# ============================================================

from flask import Flask, jsonify, request
from layers import business_logic
from layers.business_logic import BusinessRuleViolation

app = Flask(__name__)


# ------------------------------------------------------------------
# Helper — standard error response
# ------------------------------------------------------------------
STATUS_LABELS = {
    400: "400 BAD_REQUEST",
    404: "404 NOT_FOUND",
    405: "405 METHOD_NOT_ALLOWED",
    409: "409 CONFLICT",
}

def error_response(message: str, status_code: int = 400):
    label = STATUS_LABELS.get(status_code, str(status_code))
    return jsonify({"error": label, "message": message}), status_code


# ------------------------------------------------------------------
# GET /products  — list all products
# ------------------------------------------------------------------
@app.route("/products", methods=["GET"])
def list_products():
    products = business_logic.get_products()
    return jsonify({
        "total": len(products),
        "products": products
    }), 200


# ------------------------------------------------------------------
# GET /products/<id>  — get a single product
# ------------------------------------------------------------------
@app.route("/products/<product_id>", methods=["GET"])
def get_product(product_id):
    try:
        product = business_logic.get_product(product_id)
        return jsonify(product), 200
    except BusinessRuleViolation as e:
        return error_response(e.message, e.status_code)


# ------------------------------------------------------------------
# POST /orders  — place an order
# Body: { "product_id": "P001", "quantity": 2 }
# ------------------------------------------------------------------
@app.route("/orders", methods=["POST"])
def place_order():
    body = request.get_json(silent=True)

    # Guard: body must be valid JSON
    if not body:
        return error_response("Request body must be valid JSON.", 400)

    product_id = body.get("product_id")
    quantity   = body.get("quantity")

    # Guard: required fields
    if not product_id:
        return error_response("Missing required field: 'product_id'.", 400)
    if quantity is None:
        return error_response("Missing required field: 'quantity'.", 400)

    try:
        result = business_logic.place_order(product_id, quantity)
        return jsonify(result), 200
    except BusinessRuleViolation as e:
        return error_response(e.message, e.status_code)


# ------------------------------------------------------------------
# 404 catch-all
# ------------------------------------------------------------------
@app.errorhandler(404)
def not_found(_):
    return error_response("Endpoint not found. Check your URL.", 404)


# ------------------------------------------------------------------
# 405 Method Not Allowed
# ------------------------------------------------------------------
@app.errorhandler(405)
def method_not_allowed(_):
    return error_response("HTTP method not allowed on this endpoint.", 405)


# ------------------------------------------------------------------
# Entry point
# ------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 55)
    print("  Lab 3 — Business Logic API")
    print("  Running on: http://localhost:5000")
    print("=" * 55)
    app.run(debug=True, port=5000)