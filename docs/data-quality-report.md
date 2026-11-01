# Data Quality Report

This report summarizes the main data-quality issues found in the raw retail sales dataset during Sprint 002.

The raw dataset contained:

- **26,230 rows**
- **8 columns**

The goal of this review was to find data problems before the dataset is used for analysis or forecasting.

For each issue, we checked whether the value could be safely corrected. If it could not be corrected with confidence, the affected row was moved to the rejected dataset instead of guessing.
## 1. Missing Values

We found **75 missing values** in the raw dataset.

They were spread across three columns:

- `category` → 12 missing values
- `units_sold` → 35 missing values
- `stock_on_hand` → 28 missing values

We also checked whether any row had more than one missing value. The result was `0`, which means the 75 missing values were spread across **75 different rows**.

### What we did

For the 12 missing `category` values, we were able to fill them safely because those rows had known product IDs, and each known product had one consistent category.

For the 35 missing `units_sold` values, we did not guess the sales quantity, so those rows were moved to the rejected dataset.

For the 28 missing `stock_on_hand` values, we also did not guess the stock level, so those rows were moved to the rejected dataset.
## 2. Duplicate Rows

We found **22 extra duplicate rows** in the raw dataset.

When both copies of each duplicate were counted, **44 rows** were involved in total. This means there were **22 duplicate pairs**.

We also checked duplicate records using the combination of:

- `transaction_date`
- `store_id`
- `product_id`

That check also returned **22 duplicate rows**, so there were no extra repeated transaction combinations with different values.

### What we did

The extra duplicate rows were removed from the cleaned dataset and stored in the rejected dataset with the reason:

`exact duplicate row`
## 3. Negative `units_sold`

We found **16 rows** where `units_sold` was negative.

The negative values ranged from `-1` to `-7`.

Because the dataset did not explain whether negative sales represented returns, corrections, or another business process, we did not make an assumption.

### What we did

All 16 rows were moved to the rejected dataset with the reason:

`negative units_sold - business meaning unclear`
## 4. Zero `unit_price`

We found **10 rows** where `unit_price` was `0`.

We checked whether these zero-price rows could be explained by promotions.

Out of the 10 rows:

- 9 had `promotion_flag = 0`
- 1 had `promotion_flag = 1`

Because most of the zero-price rows were not marked as promotional, we could not safely assume that the products were intentionally free.

### What we did

All 10 rows were moved to the rejected dataset with the reason:

`unit_price is zero - business meaning unclear`
## 5. Invalid `promotion_flag`

We found **8 rows** where `promotion_flag` had the value `2`.

The valid values in this dataset are:

- `0` = no promotion
- `1` = promotion applied

The dataset did not explain what a value of `2` meant, so we did not try to convert it to `0` or `1`.

### What we did

All 8 rows were moved to the rejected dataset with the reason:

`promotion_flag is 2 - business meaning unclear`
## 6. `UNKNOWN` Product IDs

We found **6 rows** where `product_id` was `UNKNOWN`.

These rows appeared across different categories, including beverages, snacks, household, and personal care.

Because an `UNKNOWN` row could belong to more than one possible product, we could not safely replace it with a specific product ID.

### What we did

All 6 rows were moved to the rejected dataset with the reason:

`product_id is UNKNOWN - cannot identify reliably`
## 7. Store ID Whitespace

We found **15 rows** where `store_id` had extra spaces around the value.

For example, a value like:

`ST003 `

looks almost the same as:

`ST003`

but pandas treats them as different text values.

Before cleaning, the dataset appeared to have **8 unique store IDs**. After removing the extra spaces, it correctly had **4 stores**.

### What we did

We removed extra spaces from all `store_id` values so each store is represented consistently.
## 8. Category Formatting

The raw dataset used different text formats for the same category.

For example:

- `Beverages`
- `beverages`

and:

- `Personal_Care`
- `personal care`

These values mean the same thing, but pandas treats different text formats as different values.

### What we did

We standardized the category names by:

- removing extra spaces
- converting text to lowercase
- replacing underscores with spaces

After cleaning, the dataset had **4 consistent categories**:

- beverages
- snacks
- household
- personal care
## 9. Final Cleaning Results

After applying all cleaning rules, the dataset was split into two parts:

- **26,105 cleaned rows**
- **125 rejected rows**

The rejected rows were kept separately so that no problematic records were silently deleted.

The 125 rejected rows came from:

- 35 missing `units_sold`
- 28 missing `stock_on_hand`
- 22 duplicate rows
- 16 negative `units_sold`
- 10 zero `unit_price`
- 8 invalid `promotion_flag`
- 6 `UNKNOWN` product IDs

The final cleaned dataset has:

- no missing values
- no duplicate rows
- no negative sales values
- no zero or negative prices
- only valid promotion flags
- no unknown product IDs
- 12 valid products
- 4 categories
- 4 stores

We also confirmed that:

**26,105 cleaned rows + 125 rejected rows = 26,230 original rows**

This means no rows were accidentally lost or created during the cleaning process.
