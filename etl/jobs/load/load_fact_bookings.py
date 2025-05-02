import pandas as pd
import psycopg2
import logging
import os
import time
from etl.config import config

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/load_fact_bookings.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w",
)

CSV_PATH = "etl/data/facts/fact_bookings.csv"

CREATE_QUERY = """
    CREATE TABLE IF NOT EXISTS fact_bookings (
        booking_id BIGINT PRIMARY KEY,
        hotel_id INT,
        country_id INT,
        meal_plan_id INT,
        customer_id INT,
        arrival_year INT,
        arrival_month TEXT,
        arrival_day INT,
        lead_time BIGINT,
        weekend_nights BIGINT,
        week_nights BIGINT,
        adults BIGINT,
        children FLOAT,
        babies BIGINT,
        is_canceled INT,
        booking_changes BIGINT,
        deposit_type TEXT,
        adr FLOAT,
        parking_spaces BIGINT,
        special_requests BIGINT,
        reservation_status TEXT,
        reservation_status_date DATE
    );
"""

INSERT_QUERY = """
    INSERT INTO fact_bookings (
        booking_id, hotel_id, country_id, meal_plan_id, customer_id,
        arrival_year, arrival_month, arrival_day, lead_time,
        weekend_nights, week_nights, adults, children, babies,
        is_canceled, booking_changes, deposit_type, adr,
        parking_spaces, special_requests, reservation_status,
        reservation_status_date
    ) VALUES (
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s,
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s,
        %s, %s, %s,
        %s
    );
"""


COLUMNS_TO_INSERT = [
    "booking_id",
    "hotel_id",
    "country_id",
    "meal_plan_id",
    "customer_id",
    "arrival_year",
    "arrival_month",
    "arrival_day",
    "lead_time",
    "weekend_nights",
    "week_nights",
    "adults",
    "children",
    "babies",
    "is_canceled",
    "booking_changes",
    "deposit_type",
    "adr",
    "parking_spaces",
    "special_requests",
    "reservation_status",
    "reservation_status_date",
]


def main():
    try:
        df = pd.read_csv(CSV_PATH)
        df = df.where(pd.notnull(df), None)
        logging.info(f"Loaded {len(df)} rows from {CSV_PATH}")

        start = time.time()
        with psycopg2.connect(**config.DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(CREATE_QUERY)

                for idx, row in df[COLUMNS_TO_INSERT].iterrows():
                    try:
                        cur.execute(INSERT_QUERY, tuple(row))
                    except Exception as e:
                        logging.error(f"❌ Failed to insert row {idx}: {e}")
                        logging.warning(f"Row data: {row.to_dict()}")

        elapsed = time.time() - start
        logging.info(
            f"Inserted {len(df)} rows into fact_bookings in {elapsed:.2f} seconds."
        )
        print(f"✅ Loaded {len(df)} rows into fact_bookings in {elapsed:.2f} seconds.")

    except Exception as e:
        logging.critical(f"❌ Load failed: {e}")
        print(f"❌ Load failed: {e}")


if __name__ == "__main__":
    main()
