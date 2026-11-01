# Sprint 002 Handover

This document summarizes the work completed in Sprint 002 for the retail sales data pipeline.

The main goal of this sprint was to understand the raw dataset, identify data-quality problems, clean the data safely, and create a repeatable pipeline that can be tested and reused.

By the end of the sprint, we have:

- reviewed the raw retail sales dataset
- identified and documented data-quality issues
- created cleaning and validation scripts
- separated clean and rejected records
- added automated tests
- documented the dataset and cleaning decisions
- created a data-understanding notebook
## 1. Files Added or Updated

Sprint 002 added or updated the following project files.

### Data files

- `data/raw/Sprint_002_Retail_Sales_Data.csv`  
  Original raw dataset. This file was not changed.

- `data/processed/retail_sales_cleaned.csv`  
  Cleaned dataset containing 26,105 valid rows.

- `data/rejected/retail_sales_rejected.csv`  
  Rejected rows with a clear `rejection_reason`.

### Python files

- `src/data/load.py`  
  Loads the raw data, runs the cleaning pipeline, and saves the cleaned and rejected outputs.

- `src/data/clean.py`  
  Contains the main cleaning rules used for the dataset.

- `src/data/validate.py`  
  Contains checks used to identify common data-quality problems.

### Tests

- `tests/test_data_pipeline.py`  
  Contains automated tests that check row counts, missing values, duplicates, business rules, and rejection reasons.

### Documentation

- `notebooks/01_data_understanding.ipynb`  
  Contains the data exploration, quality checks, cleaning decisions, and final validation.

- `docs/data-dictionary.md`  
  Explains each dataset column and its cleaning rules.

- `docs/data-quality-report.md`  
  Summarizes the data-quality issues found and how they were handled.

- `docs/sprint-002-handover.md`  
  Summarizes the work completed in Sprint 002.
  ## 2. How the Data Pipeline Works

The pipeline starts with the raw CSV file and then applies the cleaning rules in a fixed order.

The flow is:

`Raw data` → `Cleaning rules` → `Cleaned data` + `Rejected data`

The main steps are:

- load the raw CSV file
- clean category values
- remove extra spaces from store IDs
- remove duplicate rows
- reject rows with missing `units_sold`
- reject rows with negative `units_sold`
- reject rows with zero `unit_price`
- reject rows with invalid `promotion_flag`
- reject rows with missing `stock_on_hand`
- reject rows with `UNKNOWN` product IDs
- convert the final columns to the correct data types
- save the cleaned and rejected datasets

The raw file is kept unchanged.
## 3. Final Data Results

The raw dataset contained **26,230 rows**.

After cleaning:

- **26,105 rows** remained in the cleaned dataset
- **125 rows** were moved to the rejected dataset

The rejected rows included:

- 35 rows with missing `units_sold`
- 28 rows with missing `stock_on_hand`
- 22 duplicate rows
- 16 rows with negative `units_sold`
- 10 rows with zero `unit_price`
- 8 rows with invalid `promotion_flag`
- 6 rows with `UNKNOWN` product IDs

We confirmed that:

**26,105 cleaned rows + 125 rejected rows = 26,230 original rows**

The final cleaned dataset also passed the main validation checks:

- no missing values
- no duplicate rows
- no negative `units_sold`
- no zero or negative `unit_price`
- no negative `stock_on_hand`
- only valid promotion flags
- no `UNKNOWN` product IDs
- 12 valid products
- 4 categories
- 4 stores
## 4. How to Run the Pipeline

From the project root folder, run:

```bash
python src/data/load.py
```

This will:

- read the raw dataset
- run the cleaning pipeline
- save the cleaned dataset
- save the rejected dataset
- print a short summary in the terminal

The expected row counts are:

- raw rows: 26,230
- cleaned rows: 26,105
- rejected rows: 125

## 5. How to Run the Tests

To check that the pipeline is working correctly, run:

```bash
python -m pytest -q
```

At the end of Sprint 002, all tests were passing.

Expected result:

```text
5 passed
```

These tests help make sure that future code changes do not accidentally break the cleaning pipeline.
