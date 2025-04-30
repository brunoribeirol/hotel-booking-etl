import pandas as pd
import psycopg2
import logging
import os
import time
from etl.config import config

SEPARATOR_LENGTH = 139
CSV_PATH = "etl/data/processed/processed_data.csv"

# Ensure the logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(
    filename="logs/load.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w",
)


def print_section(title):
    """
    Prints a section title with separators for better readability in the terminal.

    Parameters:
    title (str): The title to be printed.
    """
    print("\n" + "=" * SEPARATOR_LENGTH)
    print(title.center(SEPARATOR_LENGTH))
    print("=" * SEPARATOR_LENGTH)


def create_staging_table(cursor):
    """
    Creates the staging table in the PostgreSQL database if it doesn't exist.

    Parameters:
    cursor: A psycopg2 cursor object.
    """
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS staging_hotel_bookings (
            hotel TEXT,
            is_canceled INT,
            lead_time INT,
            arrival_year INT,
            arrival_month TEXT,
            arrival_week INT,
            arrival_day INT,
            weekend_nights INT,
            week_nights INT,
            adults INT,
            children INT,
            babies INT,
            meal_plan TEXT,
            country TEXT,
            market_segment TEXT,
            distribution_channel TEXT,
            repeated_guest INT,
            prev_cancellations INT,
            prev_not_canceled INT,
            reserved_room TEXT,
            assigned_room TEXT,
            booking_changes INT,
            deposit_type TEXT,
            agent_id TEXT,
            company_id TEXT,
            waiting_days INT,
            customer_type TEXT,
            adr FLOAT,
            parking_spaces INT,
            special_requests INT,
            reservation_status TEXT,
            reservation_status_date DATE
        );
    """
    )
    logging.info("Staging table created or confirmed to exist.")


def insert_data(df, cursor):
    """
    Inserts DataFrame rows into the staging table.

    Parameters:
    df (DataFrame): Processed data to be inserted.
    cursor: A psycopg2 cursor object.
    """
    insert_query = """
        INSERT INTO staging_hotel_bookings VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    rows_inserted = 0
    for index, row in df.iterrows():
        try:
            cursor.execute(insert_query, tuple(row))
            rows_inserted += 1
        except Exception as e:
            logging.warning(f"Row {index} insertion failed: {e}")
    return rows_inserted


def main():
    """
    Main ETL load function to load processed hotel data into PostgreSQL staging.
    """
    print_section("STARTING DATA LOAD")
    try:
        # Load the processed data
        df = pd.read_csv(CSV_PATH)
        df = df.where(pd.notnull(df), None)  # Replace NaN with None (for SQL NULL)
        logging.info(f"{len(df)} rows read from {CSV_PATH}.")

        # Start timing
        start_time = time.time()

        # Connect to the database using config
        with psycopg2.connect(**config.DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                create_staging_table(cursor)
                rows_inserted = insert_data(df, cursor)

        elapsed = time.time() - start_time
        logging.info(f"Inserted {rows_inserted} rows in {elapsed:.2f} seconds.")
        print_section("LOAD COMPLETE")
        print(
            f"✔️ {rows_inserted} rows loaded into PostgreSQL in {elapsed:.2f} seconds."
        )

    except FileNotFoundError as e:
        logging.critical(f"File not found: {e}")
        print(f"❌ File error: {e}")
    except psycopg2.Error as e:
        logging.critical(f"Database error: {e}")
        print(f"❌ Database error: {e}")
    except Exception as e:
        logging.critical(f"Unexpected error: {e}")
        print(f"❌ An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
