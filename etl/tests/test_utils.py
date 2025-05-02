from etl.jobs.utils.db_connection import get_db_connection
from etl.jobs.utils.logger import setup_logger

logger = setup_logger("test_get_db_connection", "test_get_db_connection.log")


def test_get_db_connection():
    """
    Test if the database connection can be established.
    """
    try:
        conn = get_db_connection()
        assert conn is not None, "Connection object is None."
        conn.close()
        logger.info("✅ test_get_db_connection passed.")
        print("✅ test_get_db_connection passed.")
    except Exception as e:
        logger.error(f"❌ test_get_db_connection failed: {e}")
        print(f"❌ test_get_db_connection failed: {e}")


if __name__ == "__main__":
    test_get_db_connection()
