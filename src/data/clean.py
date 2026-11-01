import pandas as pd


# ---------------------------------------------------------
# PRODUCT -> CATEGORY MAPPING
# ---------------------------------------------------------

PRODUCT_CATEGORY_MAP = {
    "P001": "beverages",
    "P002": "beverages",
    "P003": "beverages",
    "P004": "snacks",
    "P005": "snacks",
    "P006": "snacks",
    "P007": "household",
    "P008": "household",
    "P009": "household",
    "P010": "personal care",
    "P011": "personal care",
    "P012": "personal care",
}


# ---------------------------------------------------------
# CATEGORY CLEANING
# ---------------------------------------------------------

def clean_categories(data):
    cleaned_data = data.copy()

    missing_category = cleaned_data["category"].isna()

    cleaned_data.loc[
        missing_category,
        "category"
    ] = cleaned_data.loc[
        missing_category,
        "product_id"
    ].map(PRODUCT_CATEGORY_MAP)

    cleaned_data["category"] = (
        cleaned_data["category"]
        .str.strip()
        .str.lower()
        .str.replace("_", " ", regex=False)
    )

    return cleaned_data


# ---------------------------------------------------------
# STORE ID CLEANING
# ---------------------------------------------------------

def clean_store_ids(data):
    cleaned_data = data.copy()

    cleaned_data["store_id"] = (
        cleaned_data["store_id"]
        .str.strip()
    )

    return cleaned_data


# ---------------------------------------------------------
# REMOVE EXACT DUPLICATES
# ---------------------------------------------------------

def remove_duplicates(data):
    duplicate_rows = data.duplicated()

    rejected_rows = data[duplicate_rows].copy()

    rejected_rows["rejection_reason"] = (
        "exact duplicate row"
    )

    cleaned_data = data[~duplicate_rows].copy()

    return cleaned_data, rejected_rows


# ---------------------------------------------------------
# REMOVE MISSING UNITS_SOLD
# ---------------------------------------------------------

def remove_missing_units_sold(data):
    missing_units = data["units_sold"].isna()

    rejected_rows = data[missing_units].copy()

    rejected_rows["rejection_reason"] = (
        "missing units_sold"
    )

    cleaned_data = data[~missing_units].copy()

    return cleaned_data, rejected_rows


# ---------------------------------------------------------
# REMOVE NEGATIVE UNITS_SOLD
# ---------------------------------------------------------

def remove_negative_units_sold(data):
    negative_units = data["units_sold"] < 0

    rejected_rows = data[negative_units].copy()

    rejected_rows["rejection_reason"] = (
        "negative units_sold - business meaning unclear"
    )

    cleaned_data = data[~negative_units].copy()

    return cleaned_data, rejected_rows


# ---------------------------------------------------------
# REMOVE ZERO OR NEGATIVE UNIT PRICE
# ---------------------------------------------------------

def remove_nonpositive_unit_price(data):
    invalid_price = data["unit_price"] <= 0

    rejected_rows = data[invalid_price].copy()

    rejected_rows["rejection_reason"] = (
        "unit_price is zero - business meaning unclear"
    )

    cleaned_data = data[~invalid_price].copy()

    return cleaned_data, rejected_rows


# ---------------------------------------------------------
# REMOVE INVALID PROMOTION FLAGS
# ---------------------------------------------------------

def remove_invalid_promotion_flags(data):
    invalid_promotion = ~data["promotion_flag"].isin([0, 1])

    rejected_rows = data[invalid_promotion].copy()

    rejected_rows["rejection_reason"] = (
        "promotion_flag is 2 - business meaning unclear"
    )

    cleaned_data = data[~invalid_promotion].copy()

    return cleaned_data, rejected_rows


# ---------------------------------------------------------
# REMOVE MISSING STOCK_ON_HAND
# ---------------------------------------------------------

def remove_missing_stock(data):
    missing_stock = data["stock_on_hand"].isna()

    rejected_rows = data[missing_stock].copy()

    rejected_rows["rejection_reason"] = (
        "missing stock_on_hand"
    )

    cleaned_data = data[~missing_stock].copy()

    return cleaned_data, rejected_rows


# ---------------------------------------------------------
# REMOVE UNKNOWN PRODUCT IDS
# ---------------------------------------------------------

def remove_unknown_products(data):
    unknown_product = data["product_id"] == "UNKNOWN"

    rejected_rows = data[unknown_product].copy()

    rejected_rows["rejection_reason"] = (
        "product_id is UNKNOWN - cannot identify product reliably"
    )

    cleaned_data = data[~unknown_product].copy()

    return cleaned_data, rejected_rows


# ---------------------------------------------------------
# CONVERT DATA TYPES
# ---------------------------------------------------------

def convert_data_types(data):
    cleaned_data = data.copy()

    cleaned_data["transaction_date"] = pd.to_datetime(
        cleaned_data["transaction_date"],
        errors="coerce"
    )

    cleaned_data["units_sold"] = (
        cleaned_data["units_sold"]
        .astype("int64")
    )

    cleaned_data["stock_on_hand"] = (
        cleaned_data["stock_on_hand"]
        .astype("int64")
    )

    return cleaned_data


# ---------------------------------------------------------
# COMPLETE CLEANING PIPELINE
# ---------------------------------------------------------

def clean_retail_data(data):
    cleaned_data = data.copy()

    # 1. Standardize categories
    cleaned_data = clean_categories(cleaned_data)

    # 2. Remove whitespace from store IDs
    cleaned_data = clean_store_ids(cleaned_data)

    # 3. Remove exact duplicate rows
    cleaned_data, rejected_duplicates = (
        remove_duplicates(cleaned_data)
    )

    # 4. Remove rows with missing units_sold
    cleaned_data, rejected_missing_units = (
        remove_missing_units_sold(cleaned_data)
    )

    # 5. Remove rows with negative units_sold
    cleaned_data, rejected_negative_units = (
        remove_negative_units_sold(cleaned_data)
    )

    # 6. Remove rows with zero/negative unit_price
    cleaned_data, rejected_zero_price = (
        remove_nonpositive_unit_price(cleaned_data)
    )

    # 7. Remove invalid promotion flags
    cleaned_data, rejected_promotion_flag = (
        remove_invalid_promotion_flags(cleaned_data)
    )

    # 8. Remove rows with missing stock_on_hand
    cleaned_data, rejected_missing_stock = (
        remove_missing_stock(cleaned_data)
    )

    # 9. Remove UNKNOWN product IDs
    cleaned_data, rejected_unknown_product = (
        remove_unknown_products(cleaned_data)
    )

    # 10. Convert final column data types
    cleaned_data = convert_data_types(cleaned_data)

    # Combine every rejected group into one DataFrame
    rejected_data = pd.concat(
        [
            rejected_duplicates,
            rejected_missing_units,
            rejected_negative_units,
            rejected_zero_price,
            rejected_promotion_flag,
            rejected_missing_stock,
            rejected_unknown_product,
        ],
        ignore_index=True,
    )

    return cleaned_data, rejected_data
