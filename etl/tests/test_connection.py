import psycopg2
import logging
import os
from etl.config import config

# Setup logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/test_connection.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w",
)


def test_database_connection():
    try:
        conn = psycopg2.connect(**config.DB_CONFIG)
        logging.info("✅ Connection successful to hotel_dw")
        print("✅ Connection successful to hotel_dw")
        conn.close()
    except Exception as e:
        logging.error(f"❌ Connection failed: {e}")
        print(f"❌ Connection failed: {e}")


if __name__ == "__main__":
    test_database_connection()
