import pandas as pd
import psycopg2
import logging
import os
from etl.config import config
from etl.scripts.utils.logger import setup_logger
from etl.scripts.utils.db_connection import get_db_connection

logger = setup_logger("load_dim_meal", "load_dim_meal.log")
CSV_PATH = "etl/data/dimensions/dim_meal.csv"


def create_dim_table(cursor):
    """
    Creates the dim_meal table in the PostgreSQL database if it doesn't exist.
    """
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS dim_meal (
            meal_id SERIAL PRIMARY KEY,
            meal_plan TEXT NOT NULL UNIQUE
        );
        """
    )
    logger.info("dim_meal table created or already exists.")


def insert_data(df, cursor):
    """
    Inserts DataFrame rows into the dim_meal table.

    Parameters:
    - df (DataFrame): Data to insert
    - cursor: psycopg2 cursor object
    """
    insert_query = "INSERT INTO dim_meal (meal_id, meal_plan) VALUES (%s, %s) ON CONFLICT (meal_plan) DO NOTHING"
    rows_inserted = 0
    for _, row in df.iterrows():
        try:
            cursor.execute(insert_query, (row["meal_id"], row["meal_plan"]))
            rows_inserted += 1
        except Exception as e:
            logger.warning(f"Failed to insert row {row.to_dict()}: {e}")
    return rows_inserted


def main():
    try:
        logger.info("Starting dim_meal load process...")

        # Load dimension CSV
        df = pd.read_csv(CSV_PATH)
        df = df.where(pd.notnull(df), None)
        logger.info(f"Loaded {len(df)} rows from {CSV_PATH}")

        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                create_dim_table(cursor)
                inserted = insert_data(df, cursor)
                logger.info(f"Inserted {inserted} rows into dim_meal")

        print(f"✅ Loaded dim_meal with {inserted} rows.")

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
