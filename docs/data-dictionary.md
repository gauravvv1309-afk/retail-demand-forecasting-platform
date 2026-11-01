# Data Dictionary

This file explains what each column in the retail sales dataset means.

It also shows the type of data we expect in each column and any important cleaning rules we applied during Sprint 002.

The dataset contains these 8 columns:

- `transaction_date`
- `store_id`
- `product_id`
- `category`
- `units_sold`
- `unit_price`
- `promotion_flag`
- `stock_on_hand`
## 1. `transaction_date`

This column shows the date when the sale happened.

**Example:** `2025-01-01`

**Expected type:** Date

**Cleaning rule:** The value should be a valid date. We checked the raw data and found no invalid dates.

**Why it matters:** We will use this column later to study sales over time and build forecasting features.
## 2. `store_id`

This column shows which store the sale came from.

**Example:** `ST001`

**Expected type:** Text

**Cleaning rule:** Extra spaces around store IDs should be removed. In the raw data, some store IDs had hidden spaces, which made the same store look like a different value.

**Why it matters:** We use this column to compare sales between stores and understand store-level performance.
## 3. `product_id`

This column shows which product was sold.

**Example:** `P001`

**Expected type:** Text

**Cleaning rule:** The product ID should be a known product such as `P001` to `P012`. Rows with `UNKNOWN` product IDs were rejected because we could not safely identify which product they belonged to.

**Why it matters:** We use this column to track sales for each product and to understand product-level demand.
## 4. `category`

This column shows the product category.

**Example:** `beverages`

**Expected type:** Text

**Cleaning rule:** Category names were cleaned into a consistent format by removing extra spaces, changing text to lowercase, and replacing underscores with spaces.

For example:

`Personal_Care` → `personal care`

If a category was missing but the product ID was known, we filled it using the product-to-category mapping that we had already verified from the dataset.

**Why it matters:** We use this column to compare demand across different product groups.
## 5. `units_sold`

This column shows how many units of the product were sold in that transaction.

**Example:** `21`

**Expected type:** Whole number

**Cleaning rule:** Missing values were rejected because we could not safely guess how many units were sold. Negative values were also rejected because their business meaning was not clear.

After cleaning, this column contains only valid whole numbers.

**Why it matters:** This is one of the most important columns because it shows the actual demand for each product.
## 6. `unit_price`

This column shows the price of one unit of the product.

**Example:** `213.71`

**Expected type:** Decimal number

**Cleaning rule:** Prices should be greater than zero. Rows with a price of `0` were rejected because the dataset did not give enough information to confirm that those products were actually free.

**Why it matters:** We can use this column to calculate sales value and study how price changes affect demand.
## 7. `promotion_flag`

This column shows whether the product was sold under a promotion.

**Example:** `0` or `1`

**Expected type:** Whole number

**Meaning:**

- `0` = no promotion
- `1` = promotion applied

**Cleaning rule:** Only `0` and `1` are treated as valid values. Rows with a value of `2` were rejected because the dataset did not explain what `2` meant.

**Why it matters:** This column can help us understand whether promotions have an effect on product demand.
## 8. `stock_on_hand`

This column shows how many units of the product were available in stock at that time.

**Example:** `145`

**Expected type:** Whole number

**Cleaning rule:** Missing stock values were rejected because we could not safely guess the correct stock level. Negative stock values were also checked, but none were found in the raw data.

After cleaning, this column contains valid whole numbers only.

**Why it matters:** This column helps us understand whether low stock levels may affect sales and product availability.
## Summary

The cleaned dataset keeps the same 8 core columns as the raw dataset, but the values are now more consistent and reliable.

Rows with unclear or unsafe values were kept separately in the rejected dataset instead of being guessed or silently changed.

This gives us a cleaner base for the next stages of the project, including analysis, feature creation, and demand forecasting.
