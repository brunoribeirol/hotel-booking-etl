import pandas as pd
import psycopg2
import logging
import os
from etl.config import config
from etl.jobs.utils.logger import setup_logger
from etl.jobs.utils.db_connection import get_db_connection

logger = setup_logger("load_dim_country", "load_dim_country.log")
CSV_PATH = "etl/data/dimensions/dim_country.csv"


def create_dim_table(cursor):
    """
    Creates the dim_country table in the PostgreSQL database if it doesn't exist.
    """
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS dim_country (
        country_id SERIAL PRIMARY KEY,
        country_code TEXT NOT NULL UNIQUE,
        country TEXT NOT NULL
    );
    """
    )

    logger.info("dim_country table created or already exists.")


def insert_data(df, cursor):
    """
    Inserts DataFrame rows into the dim_country table.

    Parameters:
    - df (DataFrame): Data to insert
    - cursor: psycopg2 cursor object
    """
    insert_query = """
    INSERT INTO dim_country (country_id, country_code, country)
    VALUES (%s, %s, %s)
    ON CONFLICT (country_code) DO NOTHING
    """
    rows_inserted = 0
    for _, row in df.iterrows():
        try:
            cursor.execute(
                insert_query, (row["country_id"], row["country_code"], row["country"])
            )
            rows_inserted += 1
        except Exception as e:
            logger.warning(f"Failed to insert row {row.to_dict()}: {e}")
    return rows_inserted


def main():
    try:
        logger.info("Starting dim_country load process...")

        # Load dimension CSV
        df = pd.read_csv(CSV_PATH)
        df = df.where(pd.notnull(df), None)
        logger.info(f"Loaded {len(df)} rows from {CSV_PATH}")

        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                create_dim_table(cursor)
                inserted = insert_data(df, cursor)
                logger.info(f"Inserted {inserted} rows into dim_country")

        print(f"✅ Loaded dim_country with {inserted} rows.")

    except FileNotFoundError:
        logger.critical(f"File not found: {CSV_PATH}")
        print(f"❌ File not found: {CSV_PATH}")
    except psycopg2.Error as e:
        logger.critical(f"Database error: {e}")
        print(f"❌ Database error: {e}")
    except Exception as e:
        logger.critical(f"Unexpected error: {e}")
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
