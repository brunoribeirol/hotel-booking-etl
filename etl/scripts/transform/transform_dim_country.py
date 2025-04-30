import pandas as pd
import os
from etl.scripts.utils.logger import setup_logger

logger = setup_logger("transform_dim_country", "transform_dim_country.log")

INPUT_PATH = "etl/data/processed/processed_data.csv"
OUTPUT_PATH = "etl/data/dimensions/dim_country.csv"

COUNTRY_CODE_MAP = {
    "PRT": "Portugal",
    "GBR": "United Kingdom",
    "USA": "United States",
    "ESP": "Spain",
    "IRL": "Ireland",
    "FRA": "France",
    "Unknown": "Unknown",
    "ROU": "Romania",
    "NOR": "Norway",
    "OMN": "Oman",
    "ARG": "Argentina",
    "POL": "Poland",
    "DEU": "Germany",
    "BEL": "Belgium",
    "CHE": "Switzerland",
    "CHN": "China",
    "GRC": "Greece",
    "ITA": "Italy",
    "NLD": "Netherlands",
    "DNK": "Denmark",
    "RUS": "Russia",
    "SWE": "Sweden",
    "AUS": "Australia",
    "EST": "Estonia",
    "CZE": "Czech Republic",
    "BRA": "Brazil",
    "FIN": "Finland",
    "MOZ": "Mozambique",
    "BWA": "Botswana",
    "LUX": "Luxembourg",
    "SVN": "Slovenia",
    "ALB": "Albania",
    "IND": "India",
    "MEX": "Mexico",
    "MAR": "Morocco",
    "UKR": "Ukraine",
    "SMR": "San Marino",
    "LVA": "Latvia",
    "PRI": "Puerto Rico",
    "SRB": "Serbia",
    "CHL": "Chile",
    "AUT": "Austria",
    "BLR": "Belarus",
    "LTU": "Lithuania",
    "TUR": "Turkey",
    "ZAF": "South Africa",
    "AGO": "Angola",
    "ISR": "Israel",
    "CYM": "Cayman Islands",
    "ZMB": "Zambia",
    "CPV": "Cape Verde",
    "ZWE": "Zimbabwe",
    "DZA": "Algeria",
    "KOR": "South Korea",
    "CRI": "Costa Rica",
    "HUN": "Hungary",
    "ARE": "United Arab Emirates",
    "TUN": "Tunisia",
    "JAM": "Jamaica",
    "HRV": "Croatia",
    "HKG": "Hong Kong",
    "IRN": "Iran",
    "GEO": "Georgia",
    "AND": "Andorra",
    "GIB": "Gibraltar",
    "URY": "Uruguay",
    "JEY": "Jersey",
    "CAF": "Central African Republic",
    "CYP": "Cyprus",
    "COL": "Colombia",
    "GGY": "Guernsey",
    "KWT": "Kuwait",
    "NGA": "Nigeria",
    "MDV": "Maldives",
    "VEN": "Venezuela",
    "SVK": "Slovakia",
    "FJI": "Fiji",
    "KAZ": "Kazakhstan",
    "PAK": "Pakistan",
    "IDN": "Indonesia",
    "LBN": "Lebanon",
    "PHL": "Philippines",
    "SEN": "Senegal",
    "SYC": "Seychelles",
    "AZE": "Azerbaijan",
    "BHR": "Bahrain",
    "NZL": "New Zealand",
    "THA": "Thailand",
    "DOM": "Dominican Republic",
    "MKD": "North Macedonia",
    "MYS": "Malaysia",
    "ARM": "Armenia",
    "JPN": "Japan",
    "LKA": "Sri Lanka",
    "CUB": "Cuba",
    "CMR": "Cameroon",
    "BIH": "Bosnia and Herzegovina",
    "MUS": "Mauritius",
    "COM": "Comoros",
    "SUR": "Suriname",
    "UGA": "Uganda",
    "BGR": "Bulgaria",
    "CIV": "Ivory Coast",
    "JOR": "Jordan",
    "SYR": "Syria",
    "SGP": "Singapore",
    "BDI": "Burundi",
    "SAU": "Saudi Arabia",
    "VNM": "Vietnam",
    "PLW": "Palau",
    "QAT": "Qatar",
    "EGY": "Egypt",
    "PER": "Peru",
    "MLT": "Malta",
    "MWI": "Malawi",
    "ECU": "Ecuador",
    "MDG": "Madagascar",
    "ISL": "Iceland",
    "UZB": "Uzbekistan",
    "NPL": "Nepal",
    "BHS": "Bahamas",
    "MAC": "Macau",
    "TGO": "Togo",
    "TWN": "Taiwan",
    "DJI": "Djibouti",
    "STP": "Sao Tome and Principe",
    "KNA": "Saint Kitts and Nevis",
    "ETH": "Ethiopia",
    "IRQ": "Iraq",
    "HND": "Honduras",
    "RWA": "Rwanda",
    "KHM": "Cambodia",
    "MCO": "Monaco",
    "BGD": "Bangladesh",
    "IMN": "Isle of Man",
    "TJK": "Tajikistan",
    "NIC": "Nicaragua",
    "BEN": "Benin",
    "VGB": "British Virgin Islands",
    "TZA": "Tanzania",
    "GAB": "Gabon",
    "GHA": "Ghana",
    "TMP": "Timor-Leste",
    "GLP": "Guadeloupe",
    "KEN": "Kenya",
    "LIE": "Liechtenstein",
    "GNB": "Guinea-Bissau",
    "MNE": "Montenegro",
    "UMI": "United States Minor Outlying Islands",
    "MYT": "Mayotte",
    "FRO": "Faroe Islands",
    "MMR": "Myanmar",
    "PAN": "Panama",
    "BFA": "Burkina Faso",
    "LBY": "Libya",
    "MLI": "Mali",
    "NAM": "Namibia",
    "BOL": "Bolivia",
    "PRY": "Paraguay",
    "BRB": "Barbados",
    "ABW": "Aruba",
    "AIA": "Anguilla",
    "SLV": "El Salvador",
    "DMA": "Dominica",
    "PYF": "French Polynesia",
    "GUY": "Guyana",
    "LCA": "Saint Lucia",
    "ATA": "Antarctica",
    "GTM": "Guatemala",
    "ASM": "American Samoa",
    "MRT": "Mauritania",
    "NCL": "New Caledonia",
    "KIR": "Kiribati",
    "SDN": "Sudan",
    "ATF": "French Southern Territories",
    "SLE": "Sierra Leone",
    "LAO": "Laos",
}


def extract_unique_countries(df: pd.DataFrame) -> pd.DataFrame:
    unique_countries = df[["country"]].drop_duplicates().reset_index(drop=True)
    unique_countries = unique_countries.rename(columns={"country": "country_code"})
    unique_countries["country"] = unique_countries["country_code"].apply(
        lambda code: COUNTRY_CODE_MAP.get(code, f"Unknown ({code})")
    )
    unique_countries.insert(0, "country_id", range(1, len(unique_countries) + 1))
    return unique_countries


def main():
    try:
        logger.info("Reading processed data from CSV...")
        df = pd.read_csv(INPUT_PATH)

        logger.info("Extracting unique countries...")
        dim_country_df = extract_unique_countries(df)

        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
        dim_country_df.to_csv(OUTPUT_PATH, index=False)

        logger.info(f"dim_country.csv saved successfully to {OUTPUT_PATH}.")
        print("✅ dim_country.csv created successfully!")

    except Exception as e:
        logger.error(f"An error occurred during transformation: {e}")
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
