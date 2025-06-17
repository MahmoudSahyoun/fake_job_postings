import pandas as pd

# Read the CSV file
df = pd.read_csv('fake_job_postings.csv')

# Display the first 5 rows
print("\nFirst 5 rows of the data:")
print(df.head())

# Display basic information about the dataset
print("\nDataset Information:")
print(f"Number of rows: {len(df)}")
print(f"Number of columns: {len(df.columns)}")
print("\nColumn names:")
print(df.columns.tolist())

# Display data types of columns
print("\nData types of columns:")
print(df.dtypes)

# Display basic statistics for numeric columns
print("\nBasic statistics for numeric columns:")
print(df.describe()) 