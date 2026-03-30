
#================= CSV Cleaner Script =================
import pandas as pd
import os
import re
from datetime import datetime

print("\n === File Paths === ")
file_path = "./../data/online_sales_data.csv"  # input CSV
file_cleaned = "./../data/online_sales_data_clean.csv"  # cleaned CSV

print("=== 1. Check if file exists and readable ===")
if not os.path.isfile(file_path):
    raise FileNotFoundError(f"File not found: {file_path}")

try:
    df = pd.read_csv(file_path, skip_blank_lines=True)
except pd.errors.EmptyDataError:
    raise ValueError("CSV file is empty or corrupted")
except pd.errors.ParserError:
    raise ValueError("CSV file cannot be parsed properly (may be corrupted)")

print("=== Initial Data Review ===")
print("Rows x Columns:", df.shape)
print(df.head())
print(df.info())
print(df.describe(include='all'))
print(df.columns.tolist())
df_before = len(df)

print("\n === 2. Clean column names ===")
# strip spaces, lowercase, replace spaces with underscores, remove special chars
df.columns = [re.sub(r'\W+', '_', c.strip().lower()) for c in df.columns]
print("\nCleaned Columns:", df.columns.tolist())

print("\n === 3. Fill missing values for text/object columns ===")
text_columns = ['product_category', 'product_name', 'region', 'payment_method']
for col in text_columns:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip().str.title().replace({'nan':'Unknown'})
        df[col] = df[col].replace('', 'Unknown')

print("\n === 4. Parse & fill missing dates ===")
date_formats = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y", "%B %d, %Y"]

def parse_date(x):
    for fmt in date_formats:
        try:
            return pd.to_datetime(x, format=fmt)
        except:
            continue
    try:
        return pd.to_datetime(x)  # fallback
    except:
        return pd.NaT

if 'date' in df.columns:
    df['date'] = df['date'].apply(parse_date)
    # Fill missing dates with placeholder
    df['date'] = df['date'].fillna(pd.Timestamp('1970-01-01'))

print(" === 5. Clean numeric columns ===")
numeric_columns = ['units_sold', 'unit_price', 'total_revenue']
for col in numeric_columns:
    if col in df.columns:
        df[col] = df[col].astype(str).str.replace(',', '').str.replace('$','')
        df[col] = pd.to_numeric(df[col], errors='coerce')
        # Fill missing with median (units_sold, unit_price) or recalc total
        if col in ['units_sold', 'unit_price']:
            df[col] = df[col].fillna(df[col].median())
        else:
            df[col] = df[col].fillna(0)
        # Clip negatives
        df[col] = df[col].clip(lower=0)

print(" === 6. Recalculate Total Revenue ===")
if all(x in df.columns for x in ['units_sold', 'unit_price']):
    df['total_revenue'] = df['units_sold'] * df['unit_price']

print(" === 7. Trim extra spaces for object columns again ===")
for col in df.select_dtypes(include='object'):
    df[col] = df[col].str.strip().replace({'nan':'Unknown'})

print("\n === 8. Check & remove duplicates ===")
duplicates_count = df.duplicated().sum()
print("\nDuplicate rows found:", duplicates_count)
# Remove duplicates by Transaction_ID (if exists)
if 'transaction_id' in df.columns:
    df = df.drop_duplicates(subset=['transaction_id'], keep='first')
else:
    df = df.drop_duplicates(keep='first')

print(" === 9. Final checks ===")
print("\n=== Final Data Review ===")
print("Before cleaning:", df_before)
print("After cleaning :", len(df))
print("Missing values per column:\n", df.isna().sum())
print(df.head())

print(" === 10. Save cleaned CSV ===")
df.to_csv(file_cleaned, index=False)
print(f"\n✅ Cleaned CSV saved to: {file_cleaned}")