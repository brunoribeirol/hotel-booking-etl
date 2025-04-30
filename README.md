# Hotel Booking ETL Pipeline

This project implements a complete ETL (Extract, Transform, Load) pipeline for hotel booking data using Python and PostgreSQL. It includes scripts for data extraction, transformation into dimensional modeling (star schema), and loading into a PostgreSQL data warehouse. Final data can be visualized using Metabase.

---

## 📁 Project Structure

```bash
hotel-booking-etl/
├── etl/
│   ├── config/                     # Database config
│   │   └── config.py
│   ├── data/                       # Data folders
│   │   ├── raw/                    # Raw CSV input
│   │   ├── processed/              # Processed data
│   │   ├── dimensions/             # Dimension tables
│   │   └── facts/                  # Fact tables
│   ├── scripts/
│   │   ├── extract/               # Extraction logic
│   │   │   └── extract.py
│   │   ├── transform/             # Transform logic (by table)
│   │   │   ├── transform.py
│   │   │   ├── transform_dim_country.py
│   │   │   ├── transform_dim_hotel.py
│   │   │   ├── transform_dim_meal.py
│   │   │   ├── transform_dim_customer.py
│   │   │   └── transform_fact_bookings.py
│   │   ├── load/                  # Load logic (by table)
│   │   │   ├── load.py
│   │   │   ├── load_dim_country.py
│   │   │   ├── load_dim_hotel.py
│   │   │   ├── load_dim_meal.py
│   │   │   ├── load_dim_customer.py
│   │   │   └── load_fact_bookings.py
│   │   └── utils/                 # Logger and DB helpers
│   │       ├── db_connection.py
│   │       └── logger.py
├── logs/                          # Auto-generated log files
├── Makefile                       # ETL automation commands
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation
└── docs/                          # Extra documentation files
    ├── data_dictionary.pdf
    └── process_flow.pdf
```

---

## 🚀 How to Run the Project

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Start PostgreSQL (Docker)

```bash
docker-compose up -d
```

### 3. Run the ETL pipeline

```bash
make clean     # Clears DB tables and cached files
make all       # Full pipeline: extract → transform → load
```

### 4. Optional: Load Metabase

Access Metabase and connect to `hotel_dw` PostgreSQL database to create dashboards.

---

## 📊 Dashboards to Create in Metabase

- Bookings per country
- Average ADR per hotel type
- Cancellation rates over time
- Booking distribution by customer type

---

## ✅ Semantic Commit Suggestion

If this was your final working commit after implementing the whole project:

```bash
git commit -m "feat: implement full ETL pipeline with transformation and PostgreSQL load"
```

Other commits you could have used:

- `feat: add transformation scripts for dimensions and fact table`
- `fix: resolve primary key constraint issue on fact_bookings`
- `chore: update Makefile with full reset logic`

---

## 🧾 .gitignore

```gitignore
# Python artifacts
__pycache__/
*.pyc

# Logs
logs/*.log

# Data
etl/data/processed/
etl/data/dimensions/
etl/data/facts/

# Python environments
.venv/
.env

# System files
.DS_Store

# Cache
.pytest_cache/
```

---

## 📄 Docs

- `data_dictionary.pdf` — Contains descriptions for each column in dimensions and fact tables.
- `process_flow.pdf` — Shows the ETL process from raw data to PostgreSQL.

---

