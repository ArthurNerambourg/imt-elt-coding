"""
TP3 — Shared pytest fixtures
=============================
Fixtures are fake DataFrames that mimic Bronze data.
They are automatically injected into tests by pytest when a test parameter
has the same name as a fixture function.

Example:
    # This fixture is defined here:
    @pytest.fixture
    def sample_products(): ...

    # Any test with "sample_products" as a parameter receives it automatically:
    def test_something(self, sample_products):
        # sample_products is the DataFrame returned by the fixture above
"""

import pytest
import pandas as pd


@pytest.fixture
def sample_products():
    """Fake products DataFrame mimicking Bronze data."""
    return pd.DataFrame({
        "product_id": [1, 2, 3],
        "display_name": ["Nike Air Max", "Adidas Ultraboost", "Jordan 1"],
        "brand": ["Nike", "Adidas", "Jordan"],
        "category": ["sneakers", "sneakers", "sneakers"],
        "price_usd": [149.99, 179.99, -10.00],  # one invalid price for testing
        "tags": ["running|casual", "running|boost", "retro|hype"],
        "is_active": [1, 1, 0],
        "is_hype_product": [0, 0, 1],
        "_internal_cost_usd": [50.0, 60.0, 70.0],
        "_supplier_id": ["SUP001", "SUP002", "SUP003"],
    })


@pytest.fixture
def sample_users():
    """Fake users DataFrame mimicking Bronze data."""
    return pd.DataFrame({
        "user_id": [1, 2],
        "email": [" Alice@Example.COM ", "bob@test.com"],
        "first_name": ["Alice", "Bob"],
        "last_name": ["Martin", "Smith"],
        "loyalty_tier": ["gold", None],
        "_hashed_password": ["abc123", "def456"],
        "_last_ip": ["1.2.3.4", "5.6.7.8"],
        "_device_fingerprint": ["fp1", "fp2"],
    })


@pytest.fixture
def sample_orders():
    """Fake orders DataFrame mimicking Bronze data."""
    return pd.DataFrame({
        "order_id": [1, 2, 3],
        "user_id": [1, 2, 1],
        "order_date": ["2026-02-10", "2026-02-11", "2026-02-12"],
        "status": ["delivered", "shipped", "invalid_status"],
        "total_usd": [149.99, 179.99, 50.0],
        "coupon_code": ["SAVE10", None, None],
        "_stripe_charge_id": ["ch_1", "ch_2", "ch_3"],
        "_fraud_score": [0.1, 0.2, 0.9],
    })
    
@pytest.fixture
def sample_order_line_items():
    """Fake order_line_items DataFrame mimicking Bronze data."""
    return pd.DataFrame({
        "line_item_id": [101, 102, 103, 104],
        "order_id": [1, 1, 2, 3],
        "product_id": [501, 502, 501, 503],
        "selected_size": ["US 9", "US 10.5", "US 8", "L"],
        "colorway": ["Bred", "Triple White", "Chicago", "Black"],
        "quantity": [1, 2, 1, 0],
        "unit_price_usd": [149.99, 100.00, 179.99, 50.00],
        "line_total_usd": [149.99, 200.00, 179.99, 0.00],
        "_warehouse_id": ["WH-01", "WH-02", "WH-01", "WH-03"],
        "_internal_batch_code": ["BATCH-A", "BATCH-B", "BATCH-A", None],
        "_pick_slot": ["A12", "B04", "A15", "C01"]
    })
    
    
def sample_reviews():
    """Fake reviews DataFrame mimicking Bronze data."""
    return pd.DataFrame({
        "review_id": [1001, 1002, 1003, 1004],
        "product_id": [501, 502, 501, 503],
        "user_id": [1, 2, 3, 1],
        "rating": [5, 4, 1, 6],
        "title": ["Perfect fit!", "Good but tight", "Terrible experience", "CHEAP SNEAKERS HERE"],
        "body": ["Love the Chicago colorway, highly recommend.", None, "Box was completely crushed.", "Click my link to buy cheap!"], # ⚠️ Un None pour tester le body NULL
        "verified_purchase": [True, True, False, False],
        "moderation_status": ["approved", "approved", "pending", "rejected"],
        "helpful_votes": [15, 2, 0, 0],
        "_sentiment_raw": [0.95, 0.60, -0.85, 0.00],
        "_toxicity_score": [0.01, 0.05, 0.30, 0.99]
    })

@pytest.fixture
def sample_daily_revenue():
    return pd.DataFrame({
        "order_date": ["2026-02-10", "2026-02-11"],
        "total_orders": [2, 1],
        "total_revenue": [329.98, 149.99],
        "avg_order_value": [164.99, 149.99],
        "total_items": [3, 1],
    })


@pytest.fixture
def sample_product_performance():
    return pd.DataFrame({
        "product_id": [1, 2],
        "product_name": ["Nike Air Max", "Adidas Ultraboost"],
        "brand": ["Nike", "Adidas"],
        "category": ["sneakers", "sneakers"],
        "total_quantity_sold": [5, 3],
        "total_revenue": [749.95, 539.97],
        "num_orders": [4, 2],
        "avg_unit_price": [149.99, 179.99],
    })


@pytest.fixture
def sample_customer_ltv():
    return pd.DataFrame({
        "user_id": [1, 2],
        "email": ["alice@example.com", "bob@test.com"],
        "first_name": ["Alice", "Bob"],
        "last_name": ["Martin", "Smith"],
        "loyalty_tier": ["gold", "none"],
        "total_orders": [3, 1],
        "total_spent": [479.97, 179.99],
        "avg_order_value": [159.99, 179.99],
        "first_order_date": ["2026-02-10", "2026-02-11"],
        "last_order_date": ["2026-02-20", "2026-02-11"],
        "days_as_customer": [10, 0],
    })
