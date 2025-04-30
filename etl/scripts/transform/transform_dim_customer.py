import pandas as pd
import os
from etl.scripts.utils.logger import setup_logger

logger = setup_logger("transform_dim_customer", "transform_dim_customer.log")

INPUT_PATH = "etl/data/processed/processed_data.csv"
OUTPUT_PATH = "etl/data/dimensions/dim_customer.csv"


def extract_unique_customer_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extracts unique customer types from the DataFrame and assigns a surrogate key (customer_id).

    Parameters:
    df (pd.DataFrame): Processed DataFrame containing 'customer_type' column.

    Returns:
    pd.DataFrame: A DataFrame with 'customer_id' and 'customer_type' columns.
    """
    unique_values = df[["customer_type"]].drop_duplicates().reset_index(drop=True)
    unique_values.insert(0, "customer_id", range(1, len(unique_values) + 1))
    return unique_values


def main():
    """
    Reads processed data, extracts unique customer types, and saves them to a dimension CSV.
    """
    try:
        logger.info("Reading processed data from CSV...")
        df = pd.read_csv(INPUT_PATH)

        logger.info("Extracting unique customer types...")
        dim_df = extract_unique_customer_types(df)

        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
        dim_df.to_csv(OUTPUT_PATH, index=False)

        logger.info(f"dim_customer.csv saved successfully to {OUTPUT_PATH}.")
        print("✅ dim_customer.csv created successfully!")

    except Exception as e:
        logger.error(f"An error occurred during transformation: {e}")
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
