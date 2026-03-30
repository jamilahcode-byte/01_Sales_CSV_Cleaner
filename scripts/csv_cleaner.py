import pandas as pd
import os

# === File Path ===
file_path = "./../data/online_sales_data.csv"  # <-- replace with actual path
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

#review data 
print(df.head())
print(df.info())
print(df.describe())
print(df.columns)
df_before = len(df)

print("STEP 2: columns clean")
#remove strip from columns
df.columns = df.columns.str.strip().str.replace(" ", "_")
print(df.columns)

#Checks & fillna empty data
print("Checks missing values:", df.isna().sum().sum())

#fillna numbers
df["Product_Category"] = df["Product_Category"].fillna("Unknown")
df["Product_Name"] = df["Product_Name"].fillna("Unknown")
df["Region"] = df["Region"].fillna("Unknown")
df["Payment_Method"] = df["Payment_Method"].fillna("Unknown")
# Convert to datetime first
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Fill missing values with a placeholder date
df['Date'] = df['Date'].fillna(pd.Timestamp('1970-01-01'))


#to numeric change
df['Units_Sold'] = pd.to_numeric(df['Units_Sold'], errors='coerce')
df['Unit_Price'] = pd.to_numeric(df['Unit_Price'], errors='coerce')
df["Units_Sold"] = df["Units_Sold"].fillna(int(df["Units_Sold"].median()) )
df["Unit_Price"] = df["Unit_Price"].fillna(int(df["Unit_Price"].median())) 
df["Total_Revenue"] = df["Total_Revenue"].fillna(df["Units_Sold"] * df["Unit_Price"])


#Cleans rows 
for col in df.select_dtypes("object"):
    df[col] = df[col].str.strip()

print("STEP 4: Checks Duplicates & removes duplicates")
#checks duplicates 
data_dub = df.duplicated().sum()
print("Duplicateed data:", data_dub)

#remove duplicates 
df = df.drop_duplicates(subset = ["Transaction_ID"])

#Checks & review
print("Before cleaning:", df_before)
print("After cleaning:", len(df))
