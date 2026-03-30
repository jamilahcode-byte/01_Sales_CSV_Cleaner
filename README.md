Sales CSV Cleaner & Validator

Problem

Sales CSV files often contain real-world messiness:
Duplicates
Missing values
Inconsistent column names and formatting
Mixed date formats
Numeric values with commas or invalid entries
Without cleaning, analysis or automation workflows can fail or give wrong results.

Solution

A Python script using Pandas that:
Detects and removes duplicate rows
Fills missing values in text and numeric columns
Standardizes headers (strip spaces, lowercase, remove special characters)
Normalizes date columns and fills missing dates
Converts numeric columns to proper types, handles commas/invalid values
Clips negative numbers
Recalculates Total Revenue column if needed
Produces a cleaned CSV ready for analysis

Results

Applied on a sample CSV, the script:
Removed duplicate rows
Filled missing values with appropriate defaults
Standardized headers and text columns
Converted dates and numeric columns correctly
Recalculated Total Revenue
Saved cleaned CSV for analysis

Usage

Place your CSV in data/ folder
Run the script:
Bash

python scripts/csv_cleaner.py
The cleaned CSV will be saved in data/sales_data_clean.csv