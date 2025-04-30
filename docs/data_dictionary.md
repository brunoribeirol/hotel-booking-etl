# 📘 Data Dictionary - Hotel Booking ETL

This document provides a detailed overview of the fields included in the **dimension** and **fact** tables within the hotel booking ETL project.

---

## 🗂️ Dimension Tables

### `dim_hotel`

| Column   | Type | Description               |
| -------- | ---- | ------------------------- |
| hotel_id | INT  | Unique hotel identifier   |
| hotel    | TEXT | Name or code of the hotel |

---

### `dim_country`

| Column     | Type | Description                        |
| ---------- | ---- | ---------------------------------- |
| country_id | INT  | Unique identifier for each country |
| country    | TEXT | Full country name                  |

---

### `dim_meal`

| Column       | Type | Description                     |
| ------------ | ---- | ------------------------------- |
| meal_plan_id | INT  | Unique identifier for meal type |
| meal_plan    | TEXT | Description of meal plan        |

---

### `dim_customer`

| Column        | Type | Description                            |
| ------------- | ---- | -------------------------------------- |
| customer_id   | INT  | Unique customer type ID                |
| customer_type | TEXT | Category of customer (e.g., Group, TA) |

---

## 📦 Fact Table

### `fact_bookings`

| Column                  | Type             | Description                                    |
| ----------------------- | ---------------- | ---------------------------------------------- |
| booking_id              | BIGINT           | Unique identifier for each booking             |
| hotel_id                | INT              | Foreign key to `dim_hotel`                     |
| country_id              | INT              | Foreign key to `dim_country`                   |
| meal_plan_id            | INT              | Foreign key to `dim_meal`                      |
| customer_id             | INT              | Foreign key to `dim_customer`                  |
| arrival_year            | INT              | Year of arrival                                |
| arrival_month           | TEXT             | Month of arrival                               |
| arrival_day             | INT              | Day of arrival                                 |
| lead_time               | BIGINT           | Days between booking date and arrival          |
| weekend_nights          | BIGINT           | Nights on weekends                             |
| week_nights             | BIGINT           | Nights during the week                         |
| adults                  | BIGINT           | Number of adults                               |
| children                | DOUBLE PRECISION | Number of children                             |
| babies                  | BIGINT           | Number of babies                               |
| is_canceled             | INT              | 1 if booking was canceled, 0 otherwise         |
| booking_changes         | BIGINT           | Number of changes to the booking               |
| deposit_type            | TEXT             | Type of deposit (No Deposit, Non Refund, etc.) |
| adr                     | DOUBLE PRECISION | Average Daily Rate (cost per day)              |
| parking_spaces          | BIGINT           | Number of parking spaces required              |
| special_requests        | BIGINT           | Number of special requests made                |
| reservation_status      | TEXT             | Status (e.g., Canceled, No-Show, Check-Out)    |
| reservation_status_date | DATE             | Date of last reservation update                |

---

> ✅ This dictionary ensures standardized understanding of each field across the ETL and visualization layers.
