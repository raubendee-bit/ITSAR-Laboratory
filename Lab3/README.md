# ITSAR2 Laboratory Activity Business Logic API

---

## Overview

This project implements a **Product Ordering API** that demonstrates the three-layer architecture of a business system:

| Layer | File | Responsibility |
|---|---|---|
| **Presentation** | `server.py` | HTTP routing, request/response formatting |
| **Business Logic** | `layers/business_logic.py` | Order rules, validation, decision-making |
| **Data** | `layers/data_layer.py` | Product storage, stock updates |

Each layer communicates **only with the layer directly below it**. The API routes never touch the data layer directly — they always go through the business logic layer first.

---

## System Architecture Diagram

```
┌─────────────────────────────────────────────────┐
│              CLIENT (curl / Postman)            │
└────────────────────┬────────────────────────────┘
                     │  HTTP Request
                     ▼
┌─────────────────────────────────────────────────┐
│         PRESENTATION LAYER (server.py)          │
│  • Flask routes                                 │
│  • Parses request JSON                          │
│  • Formats JSON responses                       │
│  • NO business decisions made here              │
└────────────────────┬────────────────────────────┘
                     │  Calls service functions
                     ▼
┌─────────────────────────────────────────────────┐
│    BUSINESS LOGIC LAYER (business_logic.py)     │
│  • Rule 1: Product must exist                   │
│  • Rule 2: Quantity must be ≥ 1                 │
│  • Rule 3: Stock must be sufficient             │
│  • Raises BusinessRuleViolation on failure      │
└────────────────────┬────────────────────────────┘
                     │  Reads / writes
                     ▼
┌─────────────────────────────────────────────────┐
│         DATA LAYER (data_layer.py)              │
│  • In-memory product dictionary                 │
│  • get_all_products(), get_product_by_id()      │
│  • reduce_stock()                               │
└─────────────────────────────────────────────────┘
```

---

## Setup & Installation

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/lab3-business-logic-api.git
cd lab3-business-logic-api

# 2. Install dependency
pip install flask

# 3. Run the server
python server.py
```

Server starts at: `http://localhost:5000`

---

## Project Structure

```
lab3-business-logic-api/
├── server.py                  # Presentation layer (Flask routes)
├── layers/
│   ├── __init__.py
│   ├── business_logic.py      # Business logic layer (all rules)
│   └── data_layer.py          # Data layer (storage & retrieval)
└── README.md
```