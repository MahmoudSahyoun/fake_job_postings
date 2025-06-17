import pandas as pd

# === 1. Load raw data ===
df = pd.read_csv("fake_job_postings.csv")

# === 2. Select the binary flags ===
binary_flags = df[[
    "job_id",
    "telecommuting",
    "has_company_logo",
    "has_questions"
]].copy()

# (Ensure they’re 0/1 integers)
binary_flags['telecommuting'] = binary_flags['telecommuting'].astype(int)
binary_flags['has_company_logo'] = binary_flags['has_company_logo'].astype(int)
binary_flags['has_questions'] = binary_flags['has_questions'].astype(int)

# === 3. Save out ===
binary_flags.to_csv("binary_flags.csv", index=False)
print("✅ binary_flags.csv written with job_id, telecommuting, has_company_logo, has_questions")
