import pandas as pd
import os
from etl.scripts.utils.logger import setup_logger

logger = setup_logger("transform_fact_bookings", "transform_fact_bookings.log")

INPUT_PATH = "etl/data/processed/processed_data.csv"
DIM_PATH = "etl/data/dimensions"
OUTPUT_PATH = "etl/data/facts/fact_bookings.csv"


def main():
    try:
        logger.info("Reading processed data and dimension tables...")
        df = pd.read_csv(INPUT_PATH)
        dim_hotel = pd.read_csv(f"{DIM_PATH}/dim_hotel.csv")
        dim_country = pd.read_csv("etl/data/dimensions/dim_country.csv")
        dim_meal = pd.read_csv(f"{DIM_PATH}/dim_meal.csv")
        dim_customer = pd.read_csv(f"{DIM_PATH}/dim_customer.csv")

        logger.info("Merging dimension tables with processed data...")
        df = df.merge(dim_hotel, on="hotel", how="left")
        df = df.merge(dim_country[["country_code", "country_id"]], how="left", left_on="country", right_on="country_code")
        df.drop(columns=["country", "country_code"], inplace=True)
        df = df.merge(
            dim_meal.rename(columns={"meal_id": "meal_plan_id"}),
            on="meal_plan",
            how="left",
        )

        df = df.merge(dim_customer, on="customer_type", how="left")

        # Verificação de colunas obrigatórias
        required_columns = [
            "hotel_id",
            "country_id",
            "meal_plan_id",
            "customer_id",
        ]
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            logger.error(f"Missing columns after merge: {missing}")
            print(f"❌ Error: Missing columns after merge: {missing}")
            return

        logger.info("Selecting and renaming fact columns...")
        fact = df[
            [
                "hotel_id",
                "country_id",
                "meal_plan_id",
                "customer_id",
                "arrival_year",
                "arrival_month",
                "arrival_day",
                "lead_time",
                "weekend_nights",
                "week_nights",
                "adults",
                "children",
                "babies",
                "is_canceled",
                "booking_changes",
                "deposit_type",
                "adr",
                "parking_spaces",
                "special_requests",
                "reservation_status",
                "reservation_status_date",
            ]
        ].copy()

        fact.reset_index(drop=True, inplace=True)
        fact.insert(0, "booking_id", fact.index + 1)

        logger.info("Saving fact_bookings to CSV...")
        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
        fact.to_csv(OUTPUT_PATH, index=False)

        logger.info("fact_bookings.csv saved successfully.")
        print("✅ fact_bookings.csv created successfully!")

    except Exception as e:
        logger.error(f"An error occurred during fact transformation: {e}")
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
