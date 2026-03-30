import pandas as pd
import os
import re
from datetime import datetime

# === File Paths ===
file_path = "./../data/sales_data.csv"
file_cleaned = "./../data/sales_data_clean.csv"

# === 1. Check file exists and readable ===
if not os.path.isfile(file_path):
    raise FileNotFoundError(f"File not found: {file_path}")

try:
    df = pd.read_csv(file_path, skip_blank_lines=True)
except pd.errors.EmptyDataError:
    raise ValueError("CSV file is empty or corrupted")
except pd.errors.ParserError:
    raise ValueError("CSV file cannot be parsed properly")

# === 2. Remove unnamed / extra columns ===
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# === 3. Clean column names ===
df.columns = [re.sub(r'\W+', '_', c.strip().lower()) for c in df.columns]

# === 4. Handle missing text/object columns ===
text_columns = ['product_category','product_name','region','payment_method']
for col in text_columns:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip().str.title().replace({'nan':'Unknown', '':'Unknown'})

# === 5. Parse & fill dates ===
date_formats = ["%Y-%m-%d","%d/%m/%Y","%m/%d/%Y","%d-%m-%Y","%B %d, %Y"]

def parse_date(x):
    for fmt in date_formats:
        try: return pd.to_datetime(x, format=fmt)
        except: continue
    try: return pd.to_datetime(x)
    except: return pd.NaT

if 'date' in df.columns:
    df['date'] = df['date'].apply(parse_date)
    df['date'] = df['date'].fillna(pd.Timestamp('1970-01-01'))

# === 6. Clean numeric columns ===
numeric_columns = ['units_sold','unit_price','total_revenue']
for col in numeric_columns:
    if col in df.columns:
        df[col] = df[col].astype(str).str.replace(',','').str.replace('$','')
        df[col] = pd.to_numeric(df[col], errors='coerce')
        if col in ['units_sold','unit_price']:
            df[col] = df[col].fillna(df[col].median())
        else:
            df[col] = df[col].fillna(0)
        df[col] = df[col].clip(lower=0)

# === 7. Recalculate total revenue ===
if all(x in df.columns for x in ['units_sold','unit_price']):
    df['total_revenue'] = df['units_sold'] * df['unit_price']

# === 8. Trim object columns again ===
for col in df.select_dtypes(include='object'):
    df[col] = df[col].str.strip().replace({'nan':'Unknown'})

# === 9. Check & remove duplicates ===
duplicates_count = df.duplicated().sum()
print("Duplicate rows found:", duplicates_count)
if 'transaction_id' in df.columns:
    df = df.drop_duplicates(subset=['transaction_id'], keep='first')
else:
    df = df.drop_duplicates(keep='first')

# === 10. Final inspection ===
print("Rows before cleaning:", len(df))
print("Rows after cleaning :", len(df))
print("Missing values per column:\n", df.isna().sum())
print(df.head())

# === 11. Save cleaned CSV ===
df.to_csv(file_cleaned, index=False)
print(f"✅ Cleaned CSV saved to: {file_cleaned}")