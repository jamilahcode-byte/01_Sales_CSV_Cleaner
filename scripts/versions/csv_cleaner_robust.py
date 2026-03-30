import pandas as pd
import os

# === File Path ===
file_path = "your_file.csv"  # <-- replace with actual path
file_cleaned = "cleaned_file.csv"

# === 1. Detect if file exists / corrupted ===
if not os.path.isfile(file_path):
    raise FileNotFoundError(f"File not found: {file_path}")

try:
    df = pd.read_csv(file_path, skip_blank_lines=True)
except pd.errors.EmptyDataError:
    raise ValueError("CSV file is empty or corrupted")
except pd.errors.ParserError:
    raise ValueError("CSV file cannot be parsed properly (may be corrupted)")

# === 2. Remove extra unnamed columns ===
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# === 3. Inspect data ===
print("Rows and Columns:", df.shape)
print(df.head())
print(df.info())
print(df.describe(include='all'))

# === 4. Trim spaces and standardize column names ===
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
print("Columns after cleaning:", df.columns.tolist())

# === 5. Remove duplicate rows ===
print("Duplicate rows found:", df.duplicated().sum())
df = df.drop_duplicates()

# === 6. Handle missing values ===
print("Missing values per column:\n", df.isna().sum())
df = df.fillna({
    'price': 0,
    'quantity': 0,
    'date': '1970-01-01',  # placeholder for missing dates
    # add other critical columns if needed
})

# === 7. Trim extra spaces and lower text in object columns ===
for col in df.select_dtypes(include='object'):
    df[col] = df[col].astype(str).str.strip().str.lower()

# === 8. Standardize date formats ===
from datetime import datetime

formats = ["%m/%d/%Y", "%d-%m-%Y", "%Y.%m.%d", "%B %d, %Y"]

def parse_date(x):
    for fmt in formats:
        try:
            return pd.to_datetime(x, format=fmt)
        except:
            continue
    try:
        return pd.to_datetime(x)  # fallback
    except:
        return pd.NaT

if 'date' in df.columns:
    df['date_standard'] = df['date'].apply(parse_date)

# === 9. Handle numeric columns with commas or invalid values ===
for col in ['price', 'quantity']:
    if col in df.columns:
        df[col] = df[col].astype(str).str.replace(',', '')
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# === 10. Check for negative or invalid numbers ===
df['price'] = df['price'].clip(lower=0)
df['quantity'] = df['quantity'].clip(lower=0)

# === 11. Create new calculated column ===
if 'price' in df.columns and 'quantity' in df.columns:
    df['total'] = df['price'] * df['quantity']

# === 12. Final inspection ===
print(df.head())
print(df.dtypes)

# === 13. Save cleaned CSV ===
df.to_csv(file_cleaned, index=False)
print(f"Cleaned CSV saved to {file_cleaned}")