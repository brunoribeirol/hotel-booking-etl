import pandas as pd
import os
from etl.scripts.utils.logger import setup_logger

logger = setup_logger("transform_dim_hotel", "transform_dim_hotel.log")

INPUT_PATH = "etl/data/processed/processed_data.csv"
OUTPUT_PATH = "etl/data/dimensions/dim_hotel.csv"


def extract_unique_hotels(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extracts unique hotel names from the DataFrame and assigns a surrogate key (hotel_id).

    Parameters:
    df (pd.DataFrame): Processed DataFrame containing a 'hotel' column.

    Returns:
    pd.DataFrame: A DataFrame with two columns: 'hotel_id' and 'hotel'.
    """
    unique_hotels = df[["hotel"]].drop_duplicates().reset_index(drop=True)
    unique_hotels.insert(0, "hotel_id", range(1, len(unique_hotels) + 1))
    return unique_hotels


def main():
    """
    Main ETL function to transform the hotel dimension:
    - Reads the processed dataset
    - Extracts unique hotel names
    - Saves the dimension as a CSV file
    - Logs each step and handles errors gracefully
    """
    try:
        logger.info("Reading processed data from CSV...")
        df = pd.read_csv(INPUT_PATH)

        logger.info("Extracting unique hotels...")
        dim_hotel_df = extract_unique_hotels(df)

        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
        dim_hotel_df.to_csv(OUTPUT_PATH, index=False)

        logger.info(f"dim_hotel.csv saved successfully to {OUTPUT_PATH}.")
        print("✅ dim_hotel.csv created successfully!")

    except Exception as e:
        logger.error(f"An error occurred during transformation: {e}")
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
