#1. File-level Checks (Before loading)
import csv

with open(file_path, 'r', newline='') as f:
    try:
        dialect = csv.Sniffer().sniff(f.read(1024))
        f.seek(0)
        print("Delimiter detected:", dialect.delimiter)
    except csv.Error:
        print("Warning: Could not detect delimiter")

#Column-level Checks
required_columns = ['date', 'product', 'price', 'quantity']
missing_cols = [c for c in required_columns if c not in df.columns]
if missing_cols:
    print("Missing critical columns:", missing_cols)
    
#Row-level Checks
row_lengths = df.apply(lambda x: x.count(), axis=1)
if not all(row_lengths == len(df.columns)):
    print("Warning: Some rows have missing or extra columns") 

#Data-type & Value Checks
# Detect negative numbers
for col in ['price', 'quantity']:
    if (df[col] < 0).any():
        print(f"Warning: Negative values found in {col}")
        
        
#Logging / Warnings
issues = []

if df.duplicated().sum():
    issues.append(f"{df.duplicated().sum()} duplicate rows detected")
    
if df.isna().sum().sum():
    issues.append(f"{df.isna().sum().sum()} missing values found")

if issues:
    print("Data issues detected:")
    for i in issues:
        print("-", i)
                                                                                                                                                        