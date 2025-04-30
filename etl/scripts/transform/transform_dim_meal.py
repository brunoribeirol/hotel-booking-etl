import pandas as pd
import os
from etl.scripts.utils.logger import setup_logger

logger = setup_logger("transform_dim_meal", "transform_dim_meal.log")

INPUT_PATH = "etl/data/processed/processed_data.csv"
OUTPUT_PATH = "etl/data/dimensions/dim_meal.csv"


def extract_unique_meal_plans(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extracts unique meal plan types from the DataFrame and assigns a surrogate key (meal_id).

    Parameters:
    df (pd.DataFrame): Processed DataFrame containing a 'meal_plan' column.

    Returns:
    pd.DataFrame: A DataFrame with 'meal_id' and 'meal_plan' columns.
    """
    unique_meals = df[["meal_plan"]].drop_duplicates().reset_index(drop=True)
    unique_meals.insert(0, "meal_id", range(1, len(unique_meals) + 1))
    return unique_meals


def main():
    """
    Main ETL function to transform the meal plan dimension:
    - Loads the processed dataset
    - Extracts unique meal plans
    - Saves the dimension as a CSV
    - Logs progress and errors
    """
    try:
        logger.info("Reading processed data from CSV...")
        df = pd.read_csv(INPUT_PATH)

        logger.info("Extracting unique meal plans...")
        dim_meal_df = extract_unique_meal_plans(df)

        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
        dim_meal_df.to_csv(OUTPUT_PATH, index=False)

        logger.info(f"dim_meal.csv saved successfully to {OUTPUT_PATH}.")
        print("✅ dim_meal.csv created successfully!")

    except Exception as e:
        logger.error(f"An error occurred during transformation: {e}")
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
