# TP3 — Testing, Logging & Data Quality

## 📖 Context

Your ELT pipeline works end-to-end — Bronze, Silver, Gold layers are populated. But in production, "it works on my machine" is not enough. Data pipelines must be:

- **Tested**: Unit tests ensure each function works correctly in isolation
- **Observable**: Structured logs let you trace what happened when something goes wrong
- **Reliable**: Error handling prevents a single bad row from crashing the entire pipeline

In this TP, you will harden your pipeline for production readiness.

---

## 🎯 Objective

1. Write **pytest unit tests** for your transform functions (mock the database)
2. Replace `print()` with **structured logging** (JSON format)
3. Add proper **error handling** with meaningful messages
4. Aim for **≥80% test coverage** on your `src/` modules

**Files you will create / modify:**
- `tests/test_transform.py` — Unit tests for Silver transforms
- `tests/test_extract.py` — Unit tests for extraction functions
- `tests/conftest.py` — Shared pytest fixtures
- `src/transform.py`, `src/extract.py`, `src/gold.py` — Add logging + error handling

---

## 📋 Prerequisites

- TP1 & TP2 completed (full pipeline working)
- Install test dependencies:

```bash
pip install pytest pytest-cov pytest-mock
```

Add them to `requirements.txt`:
```
pytest>=7.0
pytest-cov>=4.0
pytest-mock>=3.10
```

---

## Step 1 — Unit Tests for Transform Functions (45 min)

### Principle

Unit tests verify that each function works correctly **without needing a database**. We use `unittest.mock` to replace database calls with fake data.

### 1.1 Create the test structure

```
tests/
├── __init__.py
├── conftest.py           # Shared fixtures
├── test_transform.py     # Silver layer tests
└── test_extract.py       # Bronze layer tests
```

### 1.2 Create shared fixtures (`tests/conftest.py`)

```python
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
        "price_usd": [149.99, 179.99, -10.00],  # one invalid price
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
```

### 1.3 Write transform tests (`tests/test_transform.py`)

```python
import pandas as pd
import pytest
from unittest.mock import patch, MagicMock

from src.transform import (
    _drop_internal_columns,
    transform_products,
    transform_users,
    transform_orders,
)


class TestDropInternalColumns:
    """Tests for the _drop_internal_columns() helper."""

    def test_removes_underscore_columns(self, sample_products):
        result = _drop_internal_columns(sample_products)
        assert "_internal_cost_usd" not in result.columns
        assert "_supplier_id" not in result.columns

    def test_keeps_regular_columns(self, sample_products):
        result = _drop_internal_columns(sample_products)
        assert "product_id" in result.columns
        assert "brand" in result.columns

    def test_empty_dataframe(self):
        df = pd.DataFrame()
        result = _drop_internal_columns(df)
        assert len(result.columns) == 0


class TestTransformProducts:
    """Tests for transform_products()."""

    @patch("src.transform._load_to_silver")
    @patch("src.transform._read_bronze")
    def test_removes_invalid_prices(self, mock_read, mock_load, sample_products):
        mock_read.return_value = sample_products
        result = transform_products()
        # Product with price -10.00 should be removed
        assert all(result["price_usd"] > 0)

    @patch("src.transform._load_to_silver")
    @patch("src.transform._read_bronze")
    def test_normalizes_tags(self, mock_read, mock_load, sample_products):
        mock_read.return_value = sample_products
        result = transform_products()
        # '|' should be replaced with ', '
        assert "|" not in result["tags"].str.cat()


class TestTransformUsers:
    """Tests for transform_users()."""

    @patch("src.transform._load_to_silver")
    @patch("src.transform._read_bronze")
    def test_removes_pii(self, mock_read, mock_load, sample_users):
        mock_read.return_value = sample_users
        result = transform_users()
        assert "_hashed_password" not in result.columns
        assert "_last_ip" not in result.columns
        assert "_device_fingerprint" not in result.columns

    @patch("src.transform._load_to_silver")
    @patch("src.transform._read_bronze")
    def test_fills_null_loyalty_tier(self, mock_read, mock_load, sample_users):
        mock_read.return_value = sample_users
        result = transform_users()
        assert result["loyalty_tier"].isna().sum() == 0

    @patch("src.transform._load_to_silver")
    @patch("src.transform._read_bronze")
    def test_normalizes_email(self, mock_read, mock_load, sample_users):
        mock_read.return_value = sample_users
        result = transform_users()
        assert result.iloc[0]["email"] == "alice@example.com"
```

### 1.4 Run the tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=src --cov-report=term-missing
```

**Goal:** ≥80% coverage on `src/transform.py`.

> ✅ **Checkpoint**: All tests pass, coverage ≥80%.

---

## Step 2 — Structured Logging (30 min)

### Principle

Replace `print()` statements with Python's `logging` module. In production, logs should be **structured** (JSON) so they can be parsed by monitoring tools.

### 2.1 Create a logging configuration

📁 **File:** `src/logger.py`

```python
import logging
import json
import sys
from datetime import datetime, timezone


class JSONFormatter(logging.Formatter):
    """Format log records as JSON lines."""

    def format(self, record):
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "module": record.module,
            "function": record.funcName,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_entry)


def get_logger(name: str) -> logging.Logger:
    """Create a logger with JSON output."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
```

### 2.2 Replace `print()` with logging

Example in `src/extract.py`:

```python
from src.logger import get_logger

logger = get_logger(__name__)

def extract_products():
    df = _read_csv_from_s3(f"{S3_PREFIX}/catalog/products.csv")
    logger.info(f"Products: {len(df)} rows, {len(df.columns)} columns")
    _load_to_bronze(df, "products")
    return df
```

Apply the same pattern to `src/transform.py` and `src/gold.py`.

### 2.3 Verify

Run the pipeline and observe JSON log output:

```bash
python pipeline.py --step extract
```

Expected output:
```json
{"timestamp": "2026-03-18T10:30:00Z", "level": "INFO", "module": "extract", "function": "extract_products", "message": "Products: 229 rows, 21 columns"}
```

> ✅ **Checkpoint**: All `print()` statements replaced with `logger.info()` / `logger.warning()` / `logger.error()`.

---

## Step 3 — Error Handling (20 min)

### Principle

A single bad row or network timeout should not crash the entire pipeline. Add `try/except` blocks with meaningful error messages.

### 3.1 Add error handling to extraction

```python
def extract_products():
    try:
        df = _read_csv_from_s3(f"{S3_PREFIX}/catalog/products.csv")
        logger.info(f"Products: {len(df)} rows, {len(df.columns)} columns")
        _load_to_bronze(df, "products")
        return df
    except Exception as e:
        logger.error(f"Failed to extract products: {e}")
        raise
```

### 3.2 Add error handling to transforms

```python
def transform_products():
    try:
        df = _read_bronze("products")
        df = _drop_internal_columns(df)
        # ... transformations ...
        _load_to_silver(df, "dim_products")
        return df
    except Exception as e:
        logger.error(f"Failed to transform products: {e}")
        raise
```

### 3.3 Test error scenarios

Write tests that verify error handling:

```python
class TestErrorHandling:
    @patch("src.transform._read_bronze", side_effect=Exception("DB connection lost"))
    def test_transform_products_handles_db_error(self, mock_read):
        with pytest.raises(Exception, match="DB connection lost"):
            transform_products()
```

---

## Step 4 — Test Coverage Report (15 min)

### 4.1 Generate a coverage report

```bash
pytest tests/ -v --cov=src --cov-report=html
open htmlcov/index.html
```

### 4.2 Identify untested code

Look at the coverage report and add tests for any uncovered lines. Priority targets:
- Edge cases (empty DataFrames, NULL values, invalid data)
- Error paths (database failures, S3 timeouts)
- Gold layer SQL queries (mock `pd.read_sql()`)

### 4.3 Goal

| Module | Target Coverage |
|--------|----------------|
| `src/transform.py` | ≥ 80% |
| `src/extract.py` | ≥ 70% |
| `src/gold.py` | ≥ 60% |
| `src/database.py` | ≥ 50% |

---

## 🎁 Bonus

1. **Integration tests**: Write tests that use a real database (SQLite in-memory or a test schema) to verify the full Bronze → Silver → Gold flow.
2. **Data quality assertions**: Add runtime assertions (e.g. "Gold daily_revenue total must equal Silver fct_orders total minus cancellations").
3. **Parametrized tests**: Use `@pytest.mark.parametrize` to test multiple scenarios with the same test function.
4. **Pre-commit hooks**: Set up `pre-commit` with `black`, `isort`, `flake8` to enforce code quality before each commit.

---

## 🔜 Next: TP4 — CI/CD & Industrialization

In the next TP, we will:
- Set up **GitHub Actions** to run tests automatically on every push
- Add **monitoring** and alerting for pipeline failures
- Package the pipeline for **production deployment**

---

## 📚 Resources

- [pytest Documentation](https://docs.pytest.org/en/stable/)
- [pytest-cov (Coverage)](https://pytest-cov.readthedocs.io/en/latest/)
- [unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
- [Python Logging HOWTO](https://docs.python.org/3/howto/logging.html)
- [Structured Logging Best Practices](https://www.structlog.org/en/stable/why.html)
