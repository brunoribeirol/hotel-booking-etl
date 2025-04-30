import psycopg2
import logging
from etl.config import config


def get_db_connection():
    try:
        conn = psycopg2.connect(**config.DB_CONFIG)
        logging.info("✅ PostgreSQL connection established.")
        return conn
    except psycopg2.OperationalError as e:
        logging.error(f"❌ PostgreSQL connection failed: {e}")
        raise RuntimeError(f"Database connection failed: {e}")
