from pathlib import Path
import pandas as pd
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
RAW_FILE = RAW_DATA_DIR / "Sprint_002_Retail_Sales_Data.csv"
print(RAW_FILE)
print(RAW_FILE.exists())
data = pd.read_csv(RAW_FILE)
print(data.shape)
print(data.columns)
print(data.head())
print(data.dtypes)
print(data["transaction_date"].head())
parsed_dates = pd.to_datetime(data["transaction_date"], errors="coerce")
print(parsed_dates.isna().sum())
print(parsed_dates.min())
print(parsed_dates.max())
print(data.isna().sum())
print(data.duplicated().sum())
print(data[data.duplicated(keep=False)].head(10))
print(data[data.duplicated(keep=False)].shape[0])
print((data["units_sold"] < 0).sum())
print((data["unit_price"] <= 0).sum())
print(data["promotion_flag"].value_counts(dropna=False))
print(data[data["promotion_flag"] == 2])
print((data["stock_on_hand"] < 0).sum())
print(data["category"].value_counts(dropna=False))
print((data["store_id"] != data["store_id"].str.strip()).sum())
print((data["product_id"] != data["product_id"].str.strip()).sum())
print((data["category"].fillna("") != data["category"].fillna("").str.strip()).sum())
print(
    data.loc[
        data["store_id"] != data["store_id"].str.strip(),
        "store_id"
    ].value_counts(dropna=False)
)
print(
    data.loc[
        data["store_id"] != data["store_id"].str.strip(),
        "store_id"
    ].map(repr).value_counts()
)
print(data.loc[data["unit_price"] <= 0, "unit_price"].value_counts().sort_index())
print(
    data.loc[
        data["units_sold"] < 0,
        "units_sold"
    ].value_counts().sort_index()
)
print(data.loc[data["units_sold"] < 0, "category"].value_counts(dropna=False))
print(data["store_id"].map(repr).value_counts())
print(data["store_id"].nunique())
print(data["store_id"].str.strip().nunique())
print(data["product_id"].nunique())
print(data["product_id"].value_counts().sort_index())
print(data[data["product_id"] == "UNKNOWN"])
print(data.isna().any(axis=1).sum())
print((data.isna().sum(axis=1) > 1).sum())
print(data[data["unit_price"] == 0])
print(data.loc[data["unit_price"] == 0, "promotion_flag"].value_counts())
print(
    data.loc[data["units_sold"].isna(), "store_id"]
    .str.strip()
    .value_counts()
)
print(
    data.loc[data["units_sold"].isna(), "category"]
    .str.strip()
    .str.lower()
    .str.replace("_", " ", regex=False)
    .value_counts(dropna=False)
)
print(
    data.loc[data["stock_on_hand"].isna(), "store_id"]
    .str.strip()
    .value_counts()
)
print(
    data.loc[data["stock_on_hand"].isna(), "category"]
    .str.strip()
    .str.lower()
    .str.replace("_", " ", regex=False)
    .value_counts(dropna=False)
)
print(
    data.loc[data["category"].isna(), "store_id"]
    .str.strip()
    .value_counts()
)
print(
    data.loc[data["category"].isna(), "product_id"]
    .value_counts(dropna=False)
)
print(
    data[data["category"].notna()]
    .groupby("product_id")["category"]
    .nunique()
)
print(
    data.assign(
        category_normalized=data["category"]
        .str.strip()
        .str.lower()
        .str.replace("_", " ", regex=False)
    )
    .groupby("product_id")["category_normalized"]
    .nunique()
)
print(
    data.assign(
        category_normalized=data["category"]
        .str.strip()
        .str.lower()
        .str.replace("_", " ", regex=False)
    )
    .loc[lambda x: x["product_id"] != "UNKNOWN"]
    .groupby("product_id")["category_normalized"]
    .first()
)
print(
    data.loc[
        data["category"].isna(),
        "product_id"
    ].value_counts(dropna=False)
)
print(
    data.loc[
        data["category"].isna(),
        ["product_id", "category"]
    ]
)
product_category_map = {
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
print(
    data.loc[
        data["category"].isna(),
        "product_id"
    ].map(product_category_map)
)
print(
    data.loc[
        data["category"].isna(),
        "product_id"
    ].map(product_category_map).isna().sum()
)
cleaned_data = data.copy()
missing_category = cleaned_data["category"].isna()
print(missing_category.sum())
cleaned_data.loc[
    missing_category,
    "category"
] = cleaned_data.loc[
    missing_category,
    "product_id"
].map(product_category_map)
print(cleaned_data["category"].isna().sum())
print(data["category"].isna().sum())
print(cleaned_data["category"].value_counts())
normalized_category = (
    cleaned_data["category"]
    .str.strip()
    .str.lower()
    .str.replace("_", " ", regex=False)
)
print(normalized_category.value_counts())
print(normalized_category.nunique())
cleaned_data["category"] = normalized_category
print(cleaned_data["category"].value_counts())
normalized_store_id = cleaned_data["store_id"].str.strip()
print(normalized_store_id.value_counts())
print(normalized_store_id.nunique())
cleaned_data["store_id"] = normalized_store_id
print(
    (cleaned_data["store_id"] != cleaned_data["store_id"].str.strip()).sum()
)
print(cleaned_data.duplicated().sum())
duplicate_rows = cleaned_data.duplicated()
print(duplicate_rows.sum())
all_duplicate_rows = cleaned_data.duplicated(keep=False)
print(all_duplicate_rows.sum())
duplicate_records = cleaned_data[all_duplicate_rows]
print(duplicate_records.shape)
print(duplicate_records.head(10))
print(
    cleaned_data.duplicated(
        subset=["transaction_date", "store_id", "product_id"]
    ).sum()
)
sorted_duplicates = duplicate_records.sort_values(
    by=["transaction_date", "store_id", "product_id"]
)
print(sorted_duplicates.head(6))
rejected_duplicates = cleaned_data[duplicate_rows].copy()
print(rejected_duplicates.shape)
rejected_duplicates["rejection_reason"] = "exact duplicate row"
print(rejected_duplicates["rejection_reason"].value_counts())
print((~duplicate_rows).sum())
cleaned_data = cleaned_data[~duplicate_rows].copy()
print(cleaned_data.shape)
print(cleaned_data.duplicated().sum())
print(cleaned_data["units_sold"].isna().sum())
missing_units = cleaned_data["units_sold"].isna()
print(missing_units.sum())
missing_units_records = cleaned_data[missing_units].copy()
print(missing_units_records.shape)
print(missing_units_records.head(10))
print(missing_units_records.isna().sum())
rejected_missing_units = missing_units_records.copy()
rejected_missing_units["rejection_reason"] = "missing units_sold"
print(rejected_missing_units["rejection_reason"].value_counts())
print((~missing_units).sum())
cleaned_data = cleaned_data[~missing_units].copy()
print(cleaned_data["units_sold"].isna().sum())
print((cleaned_data["units_sold"] < 0).sum())
negative_units = cleaned_data["units_sold"] < 0
negative_units_records = cleaned_data[negative_units].copy()
print(negative_units_records.shape)
print(negative_units_records)
print(negative_units_records["units_sold"].value_counts().sort_index())
rejected_negative_units = negative_units_records.copy()
rejected_negative_units["rejection_reason"] = "negative units_sold - business meaning unclear"
print(rejected_negative_units["rejection_reason"].value_counts())
print((~negative_units).sum())
cleaned_data = cleaned_data[~negative_units].copy()
print(cleaned_data.shape)
print((cleaned_data["units_sold"] < 0).sum())
print((cleaned_data["unit_price"] <= 0).sum())
zero_price_records = cleaned_data[cleaned_data["unit_price"] <= 0].copy()
print(zero_price_records)
print(zero_price_records["promotion_flag"].value_counts())
rejected_zero_price = zero_price_records.copy()
rejected_zero_price["rejection_reason"] = "unit_price is zero - business meaning unclear"
print(rejected_zero_price["rejection_reason"].value_counts())
print((cleaned_data["unit_price"] > 0).sum())
cleaned_data = cleaned_data[cleaned_data["unit_price"] > 0].copy()
print(cleaned_data.shape)
print((cleaned_data["unit_price"] <= 0).sum())
print(cleaned_data["promotion_flag"].value_counts())
promotion_flag_2 = cleaned_data["promotion_flag"] == 2
print(promotion_flag_2.sum())
promotion_flag_2_records = cleaned_data[promotion_flag_2].copy()
print(promotion_flag_2_records)
rejected_promotion_flag = promotion_flag_2_records.copy()
rejected_promotion_flag["rejection_reason"] = "promotion_flag is 2 - business meaning unclear"
print((cleaned_data["promotion_flag"] != 2).sum())
cleaned_data = cleaned_data[cleaned_data["promotion_flag"] != 2].copy()
print(cleaned_data.shape)
print(cleaned_data["promotion_flag"].value_counts())
print(cleaned_data.isna().sum())
missing_stock = cleaned_data["stock_on_hand"].isna()
print(missing_stock.sum())
missing_stock_records = cleaned_data[missing_stock].copy()
print(missing_stock_records.head(10))
print(missing_stock_records.isna().sum())
print(missing_stock_records["store_id"].value_counts())
print(missing_stock_records["category"].value_counts())
print((missing_stock.sum() / len(cleaned_data)) * 100)
rejected_missing_stock = missing_stock_records.copy()
rejected_missing_stock["rejection_reason"] = "missing stock_on_hand"
print(rejected_missing_stock["rejection_reason"].value_counts())
print((~missing_stock).sum())
cleaned_data = cleaned_data[~missing_stock].copy()
print(cleaned_data.shape)
print(cleaned_data.isna().sum())
print((cleaned_data["product_id"] == "UNKNOWN").sum())
unknown_product = cleaned_data["product_id"] == "UNKNOWN"
print(unknown_product.sum())
unknown_product_records = cleaned_data[unknown_product].copy()
print(unknown_product_records)
rejected_unknown_product = unknown_product_records.copy()
rejected_unknown_product["rejection_reason"] = "product_id is UNKNOWN - cannot identify product reliably"
print(rejected_unknown_product["rejection_reason"].value_counts())
print((~unknown_product).sum())
cleaned_data = cleaned_data[~unknown_product].copy()
print(cleaned_data.shape)
print(cleaned_data["transaction_date"].dtype)
parsed_cleaned_dates = pd.to_datetime(
    cleaned_data["transaction_date"],
    errors="coerce"
)
print(parsed_cleaned_dates.isna().sum())
cleaned_data["transaction_date"] = parsed_cleaned_dates
print(cleaned_data["transaction_date"].dtype)
print(cleaned_data["transaction_date"].min())
print(cleaned_data["transaction_date"].max())
print(cleaned_data.duplicated().sum())
print(cleaned_data.dtypes)
print((cleaned_data["units_sold"] % 1 != 0).sum())
print((cleaned_data["stock_on_hand"] % 1 != 0).sum())
cleaned_data["units_sold"] = cleaned_data["units_sold"].astype("int64")
cleaned_data["stock_on_hand"] = cleaned_data["stock_on_hand"].astype("int64")
print(cleaned_data.dtypes)
print(cleaned_data["product_id"].nunique())
print(cleaned_data["category"].nunique())
print(cleaned_data["store_id"].nunique())
print((cleaned_data["stock_on_hand"] < 0).sum())
print((cleaned_data["units_sold"] < 0).sum())
print((cleaned_data["unit_price"] <= 0).sum())
print(len(data) - len(cleaned_data))
print(
    len(rejected_duplicates)
    + len(rejected_missing_units)
    + len(rejected_negative_units)
    + len(rejected_zero_price)
    + len(rejected_promotion_flag)
    + len(rejected_missing_stock)
    + len(rejected_unknown_product)
)
rejected_data = pd.concat([
    rejected_duplicates,
    rejected_missing_units,
    rejected_negative_units,
    rejected_zero_price,
    rejected_promotion_flag,
    rejected_missing_stock,
    rejected_unknown_product
])
print(rejected_data.shape)
print(rejected_data)
print(rejected_data["rejection_reason"].value_counts())
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
print(PROCESSED_DATA_DIR.exists())
PROCESSED_FILE = PROCESSED_DATA_DIR / "retail_sales_cleaned.csv"
print(PROCESSED_FILE)
cleaned_data.to_csv(PROCESSED_FILE, index=False)
print(PROCESSED_FILE.exists())
REJECTED_DATA_DIR = PROJECT_ROOT / "data" / "rejected"
REJECTED_DATA_DIR.mkdir(parents=True, exist_ok=True)
print(REJECTED_DATA_DIR.exists())
REJECTED_FILE = REJECTED_DATA_DIR / "retail_sales_rejected.csv"
print(REJECTED_FILE)
rejected_data.to_csv(REJECTED_FILE, index=False)
print(REJECTED_FILE.exists())
saved_cleaned_data = pd.read_csv(PROCESSED_FILE)
print(saved_cleaned_data.shape)
saved_rejected_data = pd.read_csv(REJECTED_FILE)
print(saved_rejected_data.shape)
print(len(saved_cleaned_data) + len(saved_rejected_data))






