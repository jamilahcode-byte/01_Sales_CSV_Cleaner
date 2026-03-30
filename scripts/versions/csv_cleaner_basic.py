import pandas as pd

#File path 
file_path = 

#Open the CSV file
df = pd.read_csv(file_path)

#Rows data 
print(df.head()) # last by tail()
print(df.info)
print(df.describe())

#checks rows & columns 
rows, column = df.shape()
print("There are columns:", column)
print("There are rows:", rows)

#checks columns 
print(df.columns)

#Check for duplicate rows → remove them
print(df.duplicated().sum())
df = df.drop_duplicates()

#Check for missing values → fill with default or median
print(df.isna().sum().sum())
df = df.fillna("unknown")

#Trim extra spaces in text columns
for col in df.select_dtypes("object"):
    df[col] = df[col].strip().lower()
    
#Standardize date format
# List of possible date formats
formats = ["%m/%d/%Y", "%d-%m-%Y", "%Y.%m.%d", "%B %d, %Y"]
# Function to parse with multiple formats
def parse_date(x):
    for fmt in formats:
        try:
            return pd.to_datetime(x, format=fmt)
        except:
            continue
    return pd.NaT  # if none match

# Apply function
df['date_standard'] = df['date'].apply(parse_date)

#Ensure numbers (Price, Quantity) are numeric
# Convert to numeric, invalid values become NaN
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')

# Fill NaN with 0 if you want
df['Price'] = df['Price'].fillna(0)
df['Quantity'] = df['Quantity'].fillna(0)

#create new columns 
df['Total'] = df['Price'] * df['Quantity']

print(df)
print(df.dtypes)

#Save the cleaned CSV
df.to_csv(f"{file_cleaned})