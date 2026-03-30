#Read CSV File
import pandas as pd

# Load CSV
file_path = "sales_data.csv"  # replace with your file
data = pd.read_csv(file_path)

# Inspect first 5 rows
print(data.head())

#Remove Duplicate Rows
# Remove duplicates
data = data.drop_duplicates()

# Verify
print("Duplicates removed. Total rows now:", len(data))

#Handle Missing Values
# Check missing values
print(data.isnull().sum())

# Fill missing numeric columns with 0
numeric_cols = ['Quantity', 'Price', 'Total']
for col in numeric_cols:
    data[col] = data[col].fillna(0)

# Fill missing text columns with 'Unknown'
text_cols = ['Product']
for col in text_cols:
    data[col] = data[col].fillna('Unknown')

#Trim Extra Spaces & Standardize Headers
# Strip spaces in text columns
for col in text_cols:
    data[col] = data[col].str.strip()

# Standardize headers (lowercase, remove spaces)
data.columns = [col.strip().lower().replace(" ", "_") for col in data.columns]
print("Headers:", data.columns)

#Standardize Dates & Numeric Columns
# Standardize date format
data['date'] = pd.to_datetime(data['date'], errors='coerce', dayfirst=True)

# Ensure numeric columns are numbers
for col in numeric_cols:
    # Remove commas and convert to float
    data[col] = data[col].astype(str).str.replace(',', '')
    data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0)

#Export Clean CSV        
clean_path = "sales_data_clean.csv"
data.to_csv(clean_path, index=False)
print("Cleaned CSV saved to:", clean_path)    



