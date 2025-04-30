# Process Flow of the Hotel Booking ETL Pipeline

This document outlines the step-by-step process flow of the ETL (Extract, Transform, Load) pipeline used to build the Hotel Booking Data Warehouse.

---

## 1. **Extract Phase**

- **Input:** Raw dataset (CSV file) containing hotel bookings.
- **Script:** `etl/scripts/extract/extract.py`
- **Output:** `etl/data/raw/hotel_bookings.csv`
- **Description:**
  - Reads the original hotel bookings CSV file.
  - Saves a clean copy into the raw data folder for reproducibility.

---

## 2. **Transform Phase**

This phase converts raw data into structured tables suitable for analysis.

### 2.1 Processed Data Transformation

- **Script:** `etl/scripts/transform/transform.py`
- **Output:** `etl/data/processed/processed_data.csv`
- **Description:**
  - Cleans and normalizes raw data.
  - Handles missing values, data types, and formatting.

### 2.2 Dimension Tables Transformation

Each dimension has its own transformation script:

#### a) Hotel

- **Script:** `transform_dim_hotel.py`
- **Output:** `etl/data/dimensions/dim_hotel.csv`

#### b) Country

- **Script:** `transform_dim_country.py`
- **Output:** `etl/data/dimensions/dim_country.csv`

#### c) Meal Plan

- **Script:** `transform_dim_meal.py`
- **Output:** `etl/data/dimensions/dim_meal.csv`

#### d) Customer Type

- **Script:** `transform_dim_customer.py`
- **Output:** `etl/data/dimensions/dim_customer.csv`

### 2.3 Fact Table Transformation

- **Script:** `transform_fact_bookings.py`
- **Output:** `etl/data/facts/fact_bookings.csv`
- **Description:**
  - Merges processed data with all dimensions.
  - Assigns foreign keys and generates a surrogate key (booking_id).

---

## 3. **Validation Phase**

- **Script:** `validate.py`
- **Purpose:**
  - Ensures referential integrity.
  - Checks for null foreign keys or duplicated IDs.

---

## 4. **Load Phase**

Each CSV file is loaded into the PostgreSQL data warehouse.

### 4.1 Staging Table

- **Table:** `staging_hotel_bookings`
- **Script:** `load.py`

### 4.2 Dimension Tables

- **Script Folder:** `etl/scripts/load/`
  - `load_dim_hotel.py`
  - `load_dim_country.py`
  - `load_dim_meal.py`
  - `load_dim_customer.py`

### 4.3 Fact Table

- **Script:** `load_fact_bookings.py`
- **Table:** `fact_bookings`

---

## 5. **Dashboard (BI)**

- **Tool:** Metabase
- **Connection:** PostgreSQL Database (`hotel_dw`)
- **Steps:**
  - Create questions based on dimensions and facts.
  - Save queries and assemble them into dashboards.

---

## Summary Flow

```
[Raw CSV]
   ↓
[Extract]
   ↓
[Processed Data]
   ↓
[Transform Dimensions]    [Transform Fact]
   ↓                     ↓
[dim_*.csv files]       [fact_bookings.csv]
   ↓                     ↓
[Load to PostgreSQL Warehouse]
   ↓
[Metabase Dashboard]
```
