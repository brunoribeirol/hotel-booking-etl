import pandas as pd
import psycopg2
import logging
import os
from etl.config import config
from etl.scripts.utils.db_connection import get_db_connection

# Logger config
LOG_FILE = "logs/load_dim_customer.log"
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w",
)

INPUT_PATH = "etl/data/dimensions/dim_customer.csv"
TABLE_NAME = "dim_customer"


def create_table(cursor):
    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS dim_customer (
            customer_id SERIAL PRIMARY KEY,
            customer_type TEXT NOT NULL UNIQUE
        );
        """
    )
    logging.info(f"Table {TABLE_NAME} created or already exists.")


def insert_data(df, cursor):
    insert_query = f"INSERT INTO dim_customer (customer_type) VALUES (%s) ON CONFLICT (customer_type) DO NOTHING"
    rows_inserted = 0

    for index, row in df.iterrows():
        try:
            cursor.execute(insert_query, (row["customer_type"],))
            rows_inserted += 1
        except Exception as e:
            logging.warning(f"Failed to insert row {index}: {e}")

    logging.info(f"{rows_inserted} rows inserted into dim_customer.")


def main():
    """
    Loads customer dimension data into PostgreSQL.
    """
    try:
        df = pd.read_csv(INPUT_PATH)
        df = df.where(pd.notnull(df), None)

        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                create_table(cursor)
                insert_data(df, cursor)

        logging.info("dim_customer loaded successfully!")
        print("✅ dim_customer loaded successfully!")

    except Exception as e:
        logging.critical(f"Load failed: {e}")
        print(f"❌ Load failed: {e}")


if __name__ == "__main__":
    main()
