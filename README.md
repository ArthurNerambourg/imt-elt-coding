# 🏪 KICKZ EMPIRE — ELT Pipeline

## 📖 Project Description
The data used in this project comes from **KICKZ EMPIRE**, an e-commerce website specializing in sneakers and streetwear apparel. 

As Data Engineers/Data Scientists, our goal is to provide the e-commerce analytics team with clean, reliable, and aggregated data to answer critical business questions:
* *What is our daily revenue?*
* *Which products are our best-sellers?*
* *Who are our most valuable customers?*

To achieve this, we have designed and implemented a robust **ELT (Extract, Load, Transform)** pipeline.

---

## 🏗️ Architecture

Our data pipeline follows the industry-standard Medallion architecture:

```text
S3 (CSV)  ──→  🥉 Bronze (raw)  ──→  🥈 Silver (clean)  ──→  🥇 Gold (analytics)
```

| Layer | Schema | Description |
|---|---|---|
| **Bronze** | `bronze_group7` | **Raw data** — faithful copy of CSV files from S3 |
| **Silver** | `silver_group7` | **Cleaned data** — internal columns removed, data types enforced |
| **Gold** | `gold_group7` | **Aggregated data** — business-ready tables for dashboards |

---

## 🛠️ Setup Instructions

Follow these steps to configure the project locally.

**1. Clone the repository and navigate to it:**
```bash
git clone <your-repo-url>
cd imt-elt-coding
```

**2. Create and activate a virtual environment:**
* **Mac/Linux:**
  ```bash
  python -m venv venv
  source venv/bin/activate
  ```
* **Windows (Command Prompt / PowerShell):**
  ```cmd
  python -m venv venv
  venv\Scripts\Activate.ps1
  ```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Configure Environment Variables:**
Copy the template file and create your own `.env` file:
```bash
copy .env.example .env
```
Open the `.env` file and fill in your AWS and PostgreSQL credentials. 

---

## 🚀 How to Run

**1. Test the connection:**
```bash
python -m src.database
```

**2. Run the Full Pipeline:**
```bash
python pipeline.py
```

**3. Run Individual Steps:**
```bash
python pipeline.py --step extract
python pipeline.py --step transform
python pipeline.py --step load
```

---

## 🧪 How to Test

We use `pytest` to ensure our ELT pipeline works correctly.

**Run all tests:**
```bash
pytest
```

**Run tests with detailed output:**
```bash
pytest -v
```

**Run a specific test file:**
```bash
pytest tests/test_transform.py
```

---



## 📁 Project Structure

```text
├── docs/
│   ├── DATA_PRESENTATION.md    # KICKZ EMPIRE data presentation
│   └── tp1/
│       └── INSTRUCTIONS.md     # Step-by-step TP1 instructions
├── src/
│   ├── __init__.py
│   ├── database.py             # PostgreSQL connection (AWS RDS)
│   ├── extract.py              # Extract: S3 (CSV) → Bronze
│   ├── transform.py            # Transform: Bronze → Silver
│   └── gold.py                 # Gold: Silver → Gold (aggregations)
├── pipeline.py                 # ELT orchestrator
├── tests/                      # Tests (TP2)
├── .env.example                # Environment variables template
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 📊 Datasets

| Dataset | Format | Source (S3) | Bronze Table |
|---|---|---|---|
| Product Catalog | CSV | `raw/catalog/products.csv` | `products` |
| Users | CSV | `raw/users/users.csv` | `users` |
| Orders | CSV | `raw/orders/orders.csv` | `orders` |
| Order Line Items | CSV | `raw/order_line_items/order_line_items.csv` | `order_line_items` |

---

## 👥 Team Members

* **LACHGER Soufiane** - Data Engineer
* **MARTIN Sacha** - Data Engineer
* **NERAMBOURG Arthur** - Data Engineer

---