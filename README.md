# 🏨 Hotel Booking ETL Pipeline

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
│
├── docs/                          # Documentation files
│   ├── cheatsheets/
│   │   └── psql_cheatsheet.md
│   ├── kpi/                       # Visual insights and KPI dashboard
│   │   ├── images/                # Visuals used in documentation
│   │   │   ├── adr_revenue_by_hotel.png
│   │   │   ├── average_lead_time.png
│   │   │   ├── booked_nights_by_month.png
│   │   │   ├── bookings_by_country.png
│   │   │   └── cancellation_rate.png
│   │   └── kpi_dashboard.md      # KPI insights and charts
│   ├── troubleshooting/
│   │   └── postgres_docker_errors.md
│   ├── data_dictionary.md        # Describes all tables and columns
│   └── process_flow.md           # ETL process explanation/diagram
│
├── tests/                        # Unit tests for ETL components
│   ├── test_connection.py
│   ├── test_utils.py
│   └── ...
├── logs/                         # Auto-generated log files
├── Makefile                      # ETL automation commands
├── requirements.txt              # Python dependencies
├── .gitignore
├── LICENSE
├── README.md                     # Project documentation
├── docker-compose.yml
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

Access Metabase and connect to the `hotel_dw` PostgreSQL database to create dashboards.

---

## 📊 Dashboards to Create in Metabase

- Bookings per country (Region Map)
- ADR and Revenue per hotel (Bar Chart)
- Booking trends by month and hotel (Time Series)
- Lead time by country (Bar Chart)
- Cancellation rate by country (Stacked Bar)

See visual examples and analysis in [`docs/kpi/kpi_dashboard.md`](./docs/kpi/kpi_dashboard.md).

---

## 📄 Documentation

- `docs/data_dictionary.md` — Describes columns of all dimension and fact tables.
- `docs/process_flow.md` — Shows the step-by-step ETL architecture.
- `docs/kpi/kpi_dashboard.md` — Final business insights, KPIs and Metabase charts.
- `docs/cheatsheets/psql_cheatsheet.md` — Common SQL queries
- `docs/troubleshooting/postgres_docker_errors.md` — Docker/DB debugging help

---

## ✅ Requirements

- Python 3.8+
- PostgreSQL 13+
- Docker
- Metabase (optional, for dashboarding)

---

## 🌍 License

[LICENSE](LICENSE)
