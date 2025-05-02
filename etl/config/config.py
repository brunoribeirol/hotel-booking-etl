import os
from dotenv import load_dotenv

# Load .env from the root of the project
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "127.0.0.1"),
    "port": int(os.getenv("POSTGRES_PORT", "5432")),
    "dbname": os.getenv("POSTGRES_DB", "hotel_dw"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "1234"),
}

RAW_DATA = "etl/data/raw/hotel_booking.csv"
