import pandas as pd
import numpy as np
import logging
import os

# from sklearn.preprocessing import LabelEncoder

# Ensure that the "logs" directory exists
os.makedirs("logs", exist_ok=True)

# Configure logging to both console and file
logging.basicConfig(
    filename="logs/transform.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w",  # Specify write mode to overwrite the file
)


def load_data(file_path: str) -> pd.DataFrame:
    """
    Loads the dataset from the specified file path into a DataFrame.

    Parameters:
    file_path (str): The path to the CSV file to be loaded.

    Returns:
    pd.DataFrame: The loaded DataFrame.

    Raises:
    Exception: If the file cannot be loaded due to issues like missing file or parsing errors.
    """
    try:
        df = pd.read_csv(file_path)
        logging.info(f"Data loaded from {file_path}")
        return df
    except Exception as e:
        logging.error(f"Failed to load data: {e}")
        raise


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes duplicate rows from the DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to remove duplicates from.

    Returns:
    pd.DataFrame: The DataFrame without duplicate rows.
    """
    logging.info("Removing duplicate rows...")
    df = df.drop_duplicates(keep="first").reset_index(drop=True)
    # df = df.drop_duplicates()
    return df


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Renames the columns of the DataFrame to improve clarity.

    Parameters:
    df (pd.DataFrame): The original DataFrame.

    Returns:
    pd.DataFrame: The DataFrame with renamed columns.
    """
    logging.info("Renaming columns for clarity...")
    column_mapping = {
        "arrival_date_year": "arrival_year",
        "arrival_date_month": "arrival_month",
        "arrival_date_week_number": "arrival_week",
        "arrival_date_day_of_month": "arrival_day",
        "stays_in_weekend_nights": "weekend_nights",
        "stays_in_week_nights": "week_nights",
        "meal": "meal_plan",
        "is_repeated_guest": "repeated_guest",
        "previous_cancellations": "prev_cancellations",
        "previous_bookings_not_canceled": "prev_not_canceled",
        "reserved_room_type": "reserved_room",
        "assigned_room_type": "assigned_room",
        "agent": "agent_id",
        "company": "company_id",
        "days_in_waiting_list": "waiting_days",
        "required_car_parking_spaces": "parking_spaces",
        "total_of_special_requests": "special_requests",
        "phone-number": "phone_number",
    }
    return df.rename(columns=column_mapping)


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handles missing values in the DataFrame by filling them with default values.

    Parameters:
    df (pd.DataFrame): The DataFrame with missing values.

    Returns:
    pd.DataFrame: The DataFrame with missing values filled.
    """
    logging.info("Handling missing values...")
    df["children"] = df["children"].fillna(0)
    df["country"] = df["country"].fillna("Unknown")
    df["agent_id"] = df["agent_id"].fillna(-1)
    df["company_id"] = df["company_id"].fillna(-1)

    return df


def convert_to_categorical(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts specified columns to the categorical data type for memory efficiency and improved analysis.

    Parameters:
    df (pd.DataFrame): The DataFrame with columns to convert.

    Returns:
    pd.DataFrame: The DataFrame with categorical columns converted.
    """
    logging.info("Converting columns to appropriate data types...")
    categorical_columns = [
        "hotel",
        "arrival_month",
        "meal_plan",
        "country",
        "market_segment",
        "distribution_channel",
        "reservation_status",
        "reserved_room",
        "assigned_room",
        "deposit_type",
        "customer_type",
    ]

    # Ensure only existing columns are converted to category dtype
    categorical_columns = [col for col in categorical_columns if col in df.columns]

    for col in categorical_columns:
        df[col] = df[col].astype("category")

    if "reservation_status_date" in df.columns:
        df["reservation_status_date"] = pd.to_datetime(
            df["reservation_status_date"], errors="coerce"
        )

    return df


def drop_sensitive_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drops sensitive columns that should not be part of the processed data.

    Parameters:
    df (pd.DataFrame): The DataFrame containing sensitive information.

    Returns:
    pd.DataFrame: The DataFrame with sensitive columns removed.
    """
    logging.info("Dropping sensitive columns...")
    sensitive_columns = ["credit_card", "phone_number", "email", "name"]
    return df.drop(columns=[col for col in sensitive_columns if col in df.columns])


# def encode_categorical_columns(df: pd.DataFrame) -> pd.DataFrame:
#     """
#     Encodes categorical columns into numerical values using LabelEncoder.

#     Parameters:
#     df (pd.DataFrame): The DataFrame with categorical columns to encode.

#     Returns:
#     pd.DataFrame: The DataFrame with encoded categorical columns.
#     """
#     logging.info("Encoding categorical columns...")
#     label_encoder = LabelEncoder()

#     categorical_columns = [
#         col for col in df.select_dtypes(include=["category"]).columns
#     ]

#     for col in categorical_columns:
#         df[col] = label_encoder.fit_transform(df[col])

#     return df


# def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
#     """
#     Creates additional features such as 'total_stay' by combining 'weekend_nights' and 'week_nights'.

#     Parameters:
#     df (pd.DataFrame): The DataFrame to be enhanced with new features.

#     Returns:
#     pd.DataFrame: The DataFrame with additional features.
#     """
#     logging.info("Creating additional features...")
#     if "weekend_nights" in df.columns and "week_nights" in df.columns:
#         df["total_stay"] = df["weekend_nights"] + df["week_nights"]
#     else:
#         logging.warning(
#             "Columns for weekend and week nights are missing. 'total_stay' not created."
#         )

#     return df


# def convert_numerical_columns(df: pd.DataFrame) -> pd.DataFrame:
#     """
#     Converts necessary columns to numerical values, handling errors where necessary.

#     Parameters:
#     df (pd.DataFrame): The DataFrame with numerical columns to convert.

#     Returns:
#     pd.DataFrame: The DataFrame with converted numerical columns.
#     """
#     logging.info("Converting numerical columns...")
#     df["lead_time"] = pd.to_numeric(df["lead_time"], errors="coerce")
#     df["adr"] = pd.to_numeric(df["adr"], errors="coerce")
#     df["waiting_days"] = pd.to_numeric(df["waiting_days"], errors="coerce")
#     return df


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Main function that performs all data transformations including renaming columns,
    handling missing values, encoding categorical variables, and more.

    Parameters:
    df (pd.DataFrame): The raw DataFrame to transform.

    Returns:
    pd.DataFrame: The fully transformed DataFrame.
    """
    df = rename_columns(df)
    df = handle_missing_values(df)
    df = convert_to_categorical(df)
    df = drop_sensitive_columns(df)
    df = remove_duplicates(df)

    # df = convert_numerical_columns(df)
    # df = encode_categorical_columns(df)
    # df = feature_engineering(df)
    logging.info("Data transformation complete.")
    return df


def save_transformed_data(df: pd.DataFrame, output_path: str):
    """
    Saves the transformed DataFrame to a specified path as a CSV file.

    Parameters:
    df (pd.DataFrame): The transformed DataFrame to save.
    output_path (str): The path where the transformed data should be saved.

    Raises:
    Exception: If the data cannot be saved due to any issue.
    """
    try:
        df.to_csv(output_path, index=False)
        logging.info(f"Transformed data saved to {output_path}")
    except Exception as e:
        logging.error(f"Failed to save transformed data: {e}")
        raise


if __name__ == "__main__":
    # Load the dataset
    try:
        df = load_data("etl/data/raw/hotel_booking.csv")

        # Transform the data
        transformed_df = transform_data(df)

        # Ensure processed directory exists
        os.makedirs("etl/data/processed", exist_ok=True)

        # Save the transformed data
        save_transformed_data(transformed_df, "etl/data/processed/processed_data.csv")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
