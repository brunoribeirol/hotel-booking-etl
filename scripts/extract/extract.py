import pandas as pd
import logging
import os

SEPARATOR_LENGTH = 139

# Ensure that the "logs" directory exists
os.makedirs("logs", exist_ok=True)

# Configure logging to overwrite the log file on each execution
logging.basicConfig(
    filename="logs/extract.log",  # Log file name
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    filemode="w",  # Specify write mode to overwrite the file
)


def print_section(title):
    """
    Prints a section separator and title for readability.

    Parameters:
    title (str): The title to be printed within the separator.
    """
    print("\n" + "=" * SEPARATOR_LENGTH)
    print(title.center(SEPARATOR_LENGTH))
    print("=" * SEPARATOR_LENGTH)


def load_data(file_path):
    """
    Loads CSV data into a DataFrame with error handling.

    Parameters:
    file_path (str): Path to the CSV file.

    Returns:
    pd.DataFrame: The DataFrame containing the data from the CSV file.

    Raises:
    FileNotFoundError: If the file does not exist.
    pd.errors.EmptyDataError: If the file is empty.
    pd.errors.ParserError: If there is an issue parsing the CSV file.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found at path: {file_path}")

        df = pd.read_csv(file_path)
        logging.info(f"Data loaded successfully from {file_path}")
        return df
    except FileNotFoundError as e:
        logging.error(str(e))
        raise  # Re-raise the exception to allow higher-level handling
    except pd.errors.EmptyDataError:
        error_message = f"Error: The file at {file_path} is empty."
        logging.error(error_message)
        raise  # Re-raise the exception to allow higher-level handling
    except pd.errors.ParserError:
        error_message = f"Error: Failed to parse the file at {file_path}."
        logging.error(error_message)
        raise  # Re-raise the exception to allow higher-level handling
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        logging.error(error_message)
        raise  # Re-raise the exception to allow higher-level handling


def main(file_path="data/raw/hotel_booking.csv"):
    """
    Main function that loads the data, checks for missing data and duplicates,
    and logs the results.

    Parameters:
    file_path (str): Path to the CSV file to be loaded. Default is 'data/raw/hotel_booking.csv'.
    """
    try:
        # Load data
        df = load_data(file_path)

        # First 5 rows
        print_section("FIRST 5 ROWS")
        print(df.head())

        # General information
        print_section("GENERAL INFORMATION")
        df_info = df.info()
        logging.info("General info retrieved")

        # Missing data
        print_section("MISSING DATA")
        missing_data = df.isnull().sum()
        print(missing_data)
        if missing_data.any():
            logging.warning("Some columns contain missing data.")
        else:
            logging.info("No missing data detected.")

        # Duplicates
        print_section("DUPLICATES")
        duplicates = df.duplicated().sum()
        print(duplicates)
        if duplicates > 0:
            logging.warning(f"Duplicates detected: {duplicates} found.")
        else:
            logging.info("No duplicates detected.")

    except Exception as e:
        logging.critical(f"An error occurred: {e}")
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
