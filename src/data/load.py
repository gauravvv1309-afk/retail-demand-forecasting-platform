from pathlib import Path

import pandas as pd

from clean import clean_retail_data


# ---------------------------------------------------------
# PROJECT PATHS
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "Sprint_002_Retail_Sales_Data.csv"
)

PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
REJECTED_DATA_DIR = PROJECT_ROOT / "data" / "rejected"

PROCESSED_FILE = (
    PROCESSED_DATA_DIR
    / "retail_sales_cleaned.csv"
)

REJECTED_FILE = (
    REJECTED_DATA_DIR
    / "retail_sales_rejected.csv"
)


# ---------------------------------------------------------
# LOAD RAW DATA
# ---------------------------------------------------------

data = pd.read_csv(RAW_FILE)


# ---------------------------------------------------------
# CLEAN DATA
# ---------------------------------------------------------

cleaned_data, rejected_data = clean_retail_data(data)


# ---------------------------------------------------------
# CREATE OUTPUT FOLDERS
# ---------------------------------------------------------

PROCESSED_DATA_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

REJECTED_DATA_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ---------------------------------------------------------
# SAVE OUTPUT FILES
# ---------------------------------------------------------

cleaned_data.to_csv(
    PROCESSED_FILE,
    index=False,
)

rejected_data.to_csv(
    REJECTED_FILE,
    index=False,
)


# ---------------------------------------------------------
# PIPELINE SUMMARY
# ---------------------------------------------------------

print("Retail data pipeline completed successfully.")
print(f"Raw rows: {len(data)}")
print(f"Cleaned rows: {len(cleaned_data)}")
print(f"Rejected rows: {len(rejected_data)}")
print(f"Processed file: {PROCESSED_FILE}")
print(f"Rejected file: {REJECTED_FILE}")