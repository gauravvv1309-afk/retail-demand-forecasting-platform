from pathlib import Path
import pandas as pd
from src.data.clean import clean_retail_data
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "Sprint_002_Retail_Sales_Data.csv"
)
def test_cleaning_pipeline_row_counts():
    raw_data = pd.read_csv(RAW_FILE)

    cleaned_data, rejected_data = clean_retail_data(raw_data)

    assert cleaned_data.shape == (26105, 8)
    assert rejected_data.shape == (125, 9)
def test_cleaned_data_has_no_missing_values():
    raw_data = pd.read_csv(RAW_FILE)

    cleaned_data, _ = clean_retail_data(raw_data)

    assert cleaned_data.isna().sum().sum() == 0
def test_cleaned_data_has_no_duplicates():
    raw_data = pd.read_csv(RAW_FILE)

    cleaned_data, _ = clean_retail_data(raw_data)

    assert cleaned_data.duplicated().sum() == 0
def test_cleaned_data_has_valid_business_values():
    raw_data = pd.read_csv(RAW_FILE)

    cleaned_data, _ = clean_retail_data(raw_data)

    assert (cleaned_data["units_sold"] < 0).sum() == 0
    assert (cleaned_data["unit_price"] <= 0).sum() == 0
    assert (cleaned_data["stock_on_hand"] < 0).sum() == 0
    assert (~cleaned_data["promotion_flag"].isin([0, 1])).sum() == 0
    assert (cleaned_data["product_id"] == "UNKNOWN").sum() == 0
def test_rejected_data_reason_counts():
    raw_data = pd.read_csv(RAW_FILE)

    _, rejected_data = clean_retail_data(raw_data)

    reason_counts = rejected_data["rejection_reason"].value_counts()

    assert reason_counts["missing units_sold"] == 35
    assert reason_counts["missing stock_on_hand"] == 28
    assert reason_counts["exact duplicate row"] == 22
    assert reason_counts["negative units_sold - business meaning unclear"] == 16
    assert reason_counts["unit_price is zero - business meaning unclear"] == 10
    assert reason_counts["promotion_flag is 2 - business meaning unclear"] == 8
    assert reason_counts["product_id is UNKNOWN - cannot identify product reliably"] == 6
                
