import pandas as pd

# === 1. Load raw data ===
df = pd.read_csv("fake_job_postings.csv")

# === 2. Specify which columns to one-hot encode ===
cats = ['department', 'industry', 'function', 'employment_type']

# === 3. Perform one-hot encoding (including NaNs as their own column) ===
df_onehot = pd.get_dummies(df[cats], prefix=cats, dummy_na=True)

# === 4. Keep job_id for merging ===
df_onehot.insert(0, 'job_id', df['job_id'])

# === 5. Save out ===
df_onehot.to_csv("onehot_structured.csv", index=False)
print("✅ onehot_structured.csv written with one-hot columns for", cats)
