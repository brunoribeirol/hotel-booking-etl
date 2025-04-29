import pandas as pd
import logging
import os

# Ensure that the "logs" directory exists
os.makedirs("logs", exist_ok=True)

# Logging configuration
logging.basicConfig(
    filename="logs/validate.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w",  # Specify write mode to overwrite the file
)


def validate_columns(df, required_columns):
    """
    Validates if the required columns are present in the DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to be validated.
    required_columns (list): List of required columns.

    Returns:
    bool: True if all required columns are present, False otherwise.
    """
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        logging.error(f"Missing columns: {missing_columns}")
        return False
    logging.info("All required columns are present.")
    return True


def validate_data_types(df, column_types):
    """
    Validates the data types of columns in the DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to be validated.
    column_types (dict): A dictionary where the key is the column name and the value is the expected type.

    Returns:
    bool: True if all data types are correct, False otherwise.
    """
    for column, expected_type in column_types.items():
        if column in df.columns and not pd.api.types.is_dtype_equal(
            df[column].dtype, expected_type
        ):
            logging.error(
                f"Incorrect data type for column '{column}'. Expected {expected_type}, but found {df[column].dtype}."
            )
            return False
    logging.info("All data types are correct.")
    return True


def validate_missing_values(df):
    """
    Checks if there are missing values in the DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to be validated.

    Returns:
    bool: True if no missing values are found, False otherwise.
    """
    missing_values = df.isnull().sum()

    if missing_values.any():
        logging.warning(f"Missing values found: {missing_values[missing_values > 0]}")
        return False
    logging.info("No missing values found.")
    return True


def validate_duplicates(df):
    """
    Checks if there are duplicate rows in the DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to be validated.

    Returns:
    bool: True if no duplicates are found, False otherwise.
    """
    duplicates = df.duplicated().sum()

    if duplicates > 0:
        logging.warning(f"Duplicate rows found: {duplicates} records.")
        return False
    logging.info("No duplicate rows found.")
    return True


def run_validations(df):
    """
    Runs all necessary validations on the DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to be validated.

    Returns:
    bool: True if all validations pass, False otherwise.
    """
    required_columns = [
        "hotel",
        "is_canceled",
        "lead_time",
        "arrival_year",
        "arrival_month",
        "arrival_week",
        "arrival_day",
        "weekend_nights",
        "week_nights",
        "adults",
        "children",
        "babies",
        "meal_plan",
        "country",
        "market_segment",
        "distribution_channel",
        "repeated_guest",
        "prev_cancellations",
        "prev_not_canceled",
        "reserved_room",
        "assigned_room",
        "booking_changes",
        "deposit_type",
        "agent_id",
        "company_id",
        "waiting_days",
        "customer_type",
        "adr",
        "parking_spaces",
        "special_requests",
        "reservation_status",
        "reservation_status_date",
    ]

    column_types = {
        "hotel": "category",
        "is_canceled": "int64",
        "lead_time": "int64",
        "arrival_year": "int64",
        "arrival_month": "category",
        "arrival_week": "int64",
        "arrival_day": "int64",
        "weekend_nights": "int64",
        "week_nights": "int64",
        "adults": "int64",
        "children": "float64",
        "babies": "int64",
        "meal_plan": "category",
        "country": "category",
        "market_segment": "category",
        "distribution_channel": "category",
        "repeated_guest": "int64",
        "prev_cancellations": "int64",
        "prev_not_canceled": "int64",
        "reserved_room": "category",
        "assigned_room": "category",
        "booking_changes": "int64",
        "deposit_type": "category",
        "agent_id": "float64",
        "company_id": "float64",
        "waiting_days": "int64",
        "customer_type": "category",
        "adr": "float64",
        "parking_spaces": "int64",
        "special_requests": "int64",
        "reservation_status": "category",
        "reservation_status_date": "datetime64[ns]",
    }

    # Validate columns
    if not validate_columns(df, required_columns):
        return False

    # # Validate data types
    # if not validate_data_types(df, column_types):
    #     return False

    # Validate missing values
    if not validate_missing_values(df):
        return False

    # Validate duplicates
    if not validate_duplicates(df):
        return False

    logging.info("All validations were successful!")
    return True


# Example usage
if __name__ == "__main__":
    try:
        df = pd.read_csv("data/processed/processed_data.csv")
        if run_validations(df):
            logging.info("Validation completed successfully!")
        else:
            logging.error("Data validation failed.")
    except Exception as e:
        logging.error(f"Error loading data: {e}")
