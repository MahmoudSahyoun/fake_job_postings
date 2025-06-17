import pandas as pd
import numpy as np
import re

# === 1. Load Dataset ===
file_path = r'C:\Users\Sohyon\OneDrive\Desktop\Fake Job Listings\fake_job_postings.csv'
df = pd.read_csv(file_path)

# === 2. Clean company_profile Text ===
def clean_company_profile(text):
    if pd.isnull(text):
        return np.nan
    text = re.sub(r"#URL_[a-f0-9]+#", "", text)     # Remove placeholder URLs
    text = re.sub(r"#EMAIL_[a-f0-9]+#", "", text)   # Remove placeholder emails
    text = text.strip()
    return text

df['clean_company_profile'] = df['company_profile'].apply(clean_company_profile)

# === 3. Add Binary Flag Column ===
df['has_company_profile'] = df['company_profile'].notnull().astype(int)

# === 4. Save to New Excel File ===
output_columns = ['job_id', 'title', 'company_profile', 'clean_company_profile', 'has_company_profile']
output_path = r'C:\Users\Sohyon\OneDrive\Desktop\Fake Job Listings\cleaned_company_profile.xlsx'
df[output_columns].to_excel(output_path, index=False)

# === 5. Confirm Save ===
print(f"✅ Cleaned profile data saved to: {output_path}")
