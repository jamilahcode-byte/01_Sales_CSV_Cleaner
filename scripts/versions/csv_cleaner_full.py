# scripts/csv_cleaner_full.py
import pandas as pd
import os

# --- File paths ---
file_path = "data/sales_data.csv"
file_cleaned = "data/sales_data_clean.csv"

print("Step 1: Checking if file exists...")
if not os.path.isfile(file_path):
    raise FileNotFoundError(f"CSV file not found: {file_path}")
print("✅ File found:", file_path)

# --- Load CSV ---
print("\nStep 2: Loading CSV...")
try:
    df = pd.read_csv(file_path, skip_blank_lines=True)
except Exception as e:
    raise ValueError(f"Error loading CSV: {e}")
print("✅ CSV loaded successfully")
print("Initial data preview:\n", df.head())
print("Initial shape:", df.shape)

# --- Clean columns ---
print("\nStep 3: Cleaning column names...")
# Remove unnamed columns
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
# Standardize column names
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
print("Columns after cleaning:", df.columns.tolist())

# --- Check required columns ---
print("\nStep 4: Checking required columns...")
required_cols = ['date', 'product', 'price', 'quantity']
missing_cols = [c for c in required_cols if c not in df.columns]
if missing_cols:
    print(f"⚠ Warning: Missing required columns: {missing_cols}")
else:
    print("✅ All required columns are present")

# --- Detect duplicates ---
print("\nStep 5: Checking for duplicate rows...")
dup_count = df.duplicated().sum()
if dup_count:
    print(f"⚠ Found {dup_count} duplicate rows, removing...")
    df = df.drop_duplicates()
else:
    print("✅ No duplicate rows found")

# --- Detect inconsistent row lengths ---
print("\nStep 6: Checking row consistency...")
row_lengths = df.apply(lambda x: x.count(), axis=1)
if not all(row_lengths == len(df.columns)):
    print("⚠ Warning: Some rows have missing or extra columns")
else:
    print("✅ All rows consistent")

# --- Fill missing values ---
print("\nStep 7: Filling missing values...")
df = df.fillna({
    'product': 'unknown',
    'price': 0,
    'quantity': 0,
    'date': '1970-01-01'
})
print("✅ Missing values filled")
print(df.isnull().sum())

# --- Clean text columns ---
print("\nStep 8: Cleaning text columns...")
for col in df.select_dtypes(include='object'):
    df[col] = df[col].astype(str).str.strip().str.lower()
print("✅ Text columns cleaned")

# --- Parse and standardize dates ---
print("\nStep 9: Parsing dates...")
date_formats = ["%m/%d/%Y", "%d-%m-%Y", "%Y.%m.%d", "%B %d, %Y"]
def parse_date(x):
    for fmt in date_formats:
        try:
            return pd.to_datetime(x, format=fmt)
        except:
            continue
    try:
        return pd.to_datetime(x)
    except:
        return pd.NaT

if 'date' in df.columns:
    df['date_standard'] = df['date'].apply(parse_date)
    print("✅ Dates standardized. Sample:")
    print(df[['date', 'date_standard']].head())

# --- Clean numeric columns ---
print("\nStep 10: Cleaning numeric columns...")
for col in ['price', 'quantity']:
    if col in df.columns:
        df[col] = df[col].astype(str).str.replace(',', '')
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        df[col] = df[col].clip(lower=0)  # Remove negative numbers
print("✅ Numeric columns cleaned. Sample:")
print(df[['price', 'quantity']].head())

# --- Calculate total ---
print("\nStep 11: Calculating total...")
if all(c in df.columns for c in ['price', 'quantity']):
    df['total'] = df['price'] * df['quantity']
    print("✅ Total calculated. Sample:")
    print(df[['price', 'quantity', 'total']].head())

# --- Save cleaned CSV ---
print("\nStep 12: Saving cleaned CSV...")
df.to_csv(file_cleaned, index=False)
print("✅ Cleaned CSV saved to:", file_cleaned)

# --- Final summary ---
print("\nStep 13: Cleaning complete!")
print("Final shape:", df.shape)
print("Columns:", df.columns.tolist())