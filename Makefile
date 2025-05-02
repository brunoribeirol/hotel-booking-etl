# ================================
# 🛠️  Professional Makefile for ETL Pipeline
# ================================

# Variables
LOG_DIR=logs
DB_CONTAINER=hotel_postgres
DB_USER=postgres
DB_NAME=hotel_dw

# Targets that don't represent real files
.PHONY: help extract transform validate load all clean \
        transform-hotel transform-country transform-meal transform-customer transform-dimensions transform-fact \
        load-hotel load-country load-meal load-customer load-dimensions load-fact

# ---------------------------------------
# 🧾 Help: Lists all available commands
# ---------------------------------------
help:
	@echo "Available make commands:"
	@echo "  make extract               - Run the data extraction step"
	@echo "  make transform             - Run the main data transformation step"
	@echo "  make transform-dimensions  - Run all dimension transformations"
	@echo "  make transform-hotel       - Transform hotel dimension"
	@echo "  make transform-country     - Transform country dimension"
	@echo "  make transform-meal        - Transform meal plan dimension"
	@echo "  make transform-customer    - Transform customer type dimension"
	@echo "  make transform-fact        - Transform fact table"
	@echo "  make validate              - Run data validation"
	@echo "  make load                  - Load staging data into PostgreSQL"
	@echo "  make load-dimensions       - Load all dimension tables"
	@echo "  make load-hotel            - Load hotel dimension into PostgreSQL"
	@echo "  make load-country          - Load country dimension into PostgreSQL"
	@echo "  make load-meal             - Load meal plan dimension into PostgreSQL"
	@echo "  make load-customer         - Load customer type dimension into PostgreSQL"
	@echo "  make load-fact             - Load fact table into PostgreSQL"
	@echo "  make all                   - Run full pipeline (extract → transform → dimensions → validate → load)"
	@echo "  make clean                 - Drop database tables and remove temporary files"

# ---------------------------------------
# 🍉 Extraction Step
# ---------------------------------------
extract:
	@echo "🔍 Starting extraction..."
	@PYTHONPATH=. python -m etl.jobs.extract.extract
	@echo "✅ Extraction complete."

# ---------------------------------------
# 🔨 Transformation Step
# ---------------------------------------
transform:
	@echo "🔧 Starting transformation..."
	@PYTHONPATH=. python -m etl.jobs.transform.transform
	@echo "✅ Transformation complete."

transform-hotel:
	@PYTHONPATH=. python -m etl.jobs.transform.transform_dim_hotel

transform-country:
	@PYTHONPATH=. python -m etl.jobs.transform.transform_dim_country

transform-meal:
	@PYTHONPATH=. python -m etl.jobs.transform.transform_dim_meal

transform-customer:
	@PYTHONPATH=. python -m etl.jobs.transform.transform_dim_customer

transform-fact:
	@PYTHONPATH=. python -m etl.jobs.transform.transform_fact_bookings

transform-dimensions: transform-hotel transform-country transform-meal transform-customer transform-fact
	@echo "✅ All dimension and fact transformations complete."

# ---------------------------------------
# 🧪 Validation Step
# ---------------------------------------
validate:
	@echo "🔎 Starting validation..."
	@PYTHONPATH=. python -m etl.jobs.transform.validate
	@echo "✅ Validation complete."

# ---------------------------------------
# 🗄️ Load Step
# ---------------------------------------
load:
	@echo "📄 Loading staging data to PostgreSQL..."
	@PYTHONPATH=. python -m etl.jobs.load.load
	@echo "✅ Staging load complete."

load-hotel:
	@PYTHONPATH=. python -m etl.jobs.load.load_dim_hotel

load-country:
	@PYTHONPATH=. python -m etl.jobs.load.load_dim_country

load-meal:
	@PYTHONPATH=. python -m etl.jobs.load.load_dim_meal

load-customer:
	@PYTHONPATH=. python -m etl.jobs.load.load_dim_customer

load-fact:
	@PYTHONPATH=. python -m etl.jobs.load.load_fact_bookings

load-dimensions: load-hotel load-country load-meal load-customer load-fact
	@echo "✅ All dimension and fact loads complete."

# ---------------------------------------
# 🚀 Full ETL Pipeline
# ---------------------------------------
all: extract transform transform-dimensions validate load load-dimensions

# ---------------------------------------
# 🧹 Clean project (including PostgreSQL tables)
# ---------------------------------------
clean:
	@echo "🧹 Dropping tables in PostgreSQL and cleaning files..."
	@docker exec -i $(DB_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME) -c "DROP TABLE IF EXISTS fact_bookings, dim_country, dim_customer, dim_hotel, dim_meal, staging_hotel_bookings CASCADE;"
	@rm -f logs/*.log
	@rm -f etl/data/processed/*.csv
	@rm -f etl/data/dimensions/*.csv
	@rm -f etl/data/facts/*.csv
	@find . -type d -name '__pycache__' -exec rm -r {} +
	@find . -type f -name '*.pyc' -delete
	@rm -rf .pytest_cache
	@echo "✅ Project fully cleaned."
