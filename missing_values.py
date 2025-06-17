import pandas as pd

# === 1. Load the Dataset ===
file_path = r'C:\Users\Sohyon\OneDrive\Desktop\Fake Job Listings\fake_job_postings.csv'
df = pd.read_csv(file_path)

# === 2. Show Shape ===
print("✅ Dataset Shape:")
print(df.shape)  # (rows, columns)

# === 3. Preview First 5 Rows ===
print("\n📊 First 5 Rows:")
print(df.head())

# === 4. Check Missing Values Per Column ===
print("\n❓ Missing Values Per Column:")
missing_counts = df.isnull().sum().sort_values(ascending=False)
print(missing_counts)

# === 5. Optional: Show Columns with More Than 50% Missing ===
print("\n⚠️ Columns with >50% Missing Values:")
print(missing_counts[missing_counts > len(df) * 0.5])
