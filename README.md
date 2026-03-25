# KICKZ EMPIRE — ELT Pipeline

ELT (Extract, Load, Transform) pipeline for the **KICKZ EMPIRE** e-commerce website, built as part of the IMT Data Engineering course. Our goal as data scientists is to provide the e-commerce team with clear, clean data to answer the following questions: 

What is our daily revenue?
Which products sell best?
Who are our best customers?

## 🏗️ Architecture

```
S3 (CSV)  ──→  🥉 Bronze (raw)  ──→  🥈 Silver (clean)  ──→  🥇 Gold (analytics)
```

| Layer | Schema | Description |
|---|---|---|
| **Bronze** | `bronze_groupN` | Raw data — faithful copy of CSV files from S3 |
| **Silver** | `silver_groupN` | Cleaned data — internal columns removed, PII masked |
| **Gold** | `gold_groupN` | Aggregated data — ready for dashboards |

## 📁 Project Structure

```
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

## 🚀 Quick Start

```bash
# 1. Setup
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Configure with your credentials (DB + AWS)

# 2. Test the connection
python -m src.database

# 3. Run the pipeline (reads from S3 automatically)
python pipeline.py
```

## 📊 Datasets

| Dataset | Format | Source (S3) | Bronze Table |
|---|---|---|---|
| Product Catalog | CSV | `raw/catalog/products.csv` | `products` |
| Users | CSV | `raw/users/users.csv` | `users` |
| Orders | CSV | `raw/orders/orders.csv` | `orders` |
| Order Line Items | CSV | `raw/order_line_items/order_line_items.csv` | `order_line_items` |

## 📚 Documentation

- [Data Presentation](docs/DATA_PRESENTATION.md)
- [TP1 Instructions](docs/tp1/INSTRUCTIONS.md)

## ⚙️ Tech Stack

- **Python 3.10+** : Main language
- **pandas** : Data manipulation
- **boto3** : AWS S3 access
- **SQLAlchemy** : ORM / PostgreSQL connection
- **PostgreSQL** (AWS RDS) : Database
- **pytest** : Testing (TP2)


Instructions d'installation (étape par étape)
Comment exécuter (pipeline complet + étapes individuelles)

Test de l'ELT : 
Pour tester le fonctionnement de l'ELT 


## Team members 
LACHGER Soufiane
MARTIN Sacha 
NERAMBOURG Arthur


