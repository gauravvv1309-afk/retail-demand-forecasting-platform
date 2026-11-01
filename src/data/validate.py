import pandas as pd
REQUIRED_COLUMNS = [
    "transaction_date",
    "store_id",
    "product_id",
    "category",
    "units_sold",
    "unit_price",
    "promotion_flag",
    "stock_on_hand",
]
def check_required_columns(data):
    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in data.columns
    ]

    return missing_columns
def count_missing_values(data):
    return data.isna().sum()
def count_duplicate_rows(data):
    return data.duplicated().sum()
def count_negative_units_sold(data):
    return (data["units_sold"] < 0).sum()
def count_nonpositive_unit_price(data):
    return (data["unit_price"] <= 0).sum()
def count_invalid_promotion_flags(data):
    return (~data["promotion_flag"].isin([0, 1])).sum()
def count_negative_stock(data):
    return (data["stock_on_hand"] < 0).sum()
def count_unknown_product_ids(data):
    return (data["product_id"] == "UNKNOWN").sum()
def count_invalid_dates(data):
    parsed_dates = pd.to_datetime(
        data["transaction_date"],
        errors="coerce"
    )

    return parsed_dates.isna().sum()
def count_store_id_whitespace(data):
    stripped_store_ids = data["store_id"].str.strip()

    return (data["store_id"] != stripped_store_ids).sum()
