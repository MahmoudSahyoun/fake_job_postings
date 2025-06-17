import pandas as pd
import numpy as np
import re
import html

# === 1. Load dataset ===
file_path = r'C:\Users\Sohyon\OneDrive\Desktop\Fake Job Listings\fake_job_postings.csv'
df = pd.read_csv(file_path)

# === 2. Clean description ===
def clean_description(text):
    if pd.isnull(text):
        return np.nan
    if text.strip() == "#NAME?":
        return np.nan
    text = re.sub(r"#URL_[a-f0-9]+#", "", text)        # Remove URL placeholders
    text = html.unescape(text)                         # Convert HTML entities like &nbsp;
    text = text.strip()
    return text

df['clean_description'] = df['description'].apply(clean_description)

# === 3. Add word count and flag columns ===
df['description_word_count'] = df['clean_description'].apply(lambda x: len(str(x).split()) if pd.notnull(x) else 0)
df['has_description'] = df['description'].notnull().astype(int)

# === 4. Save cleaned descriptions to new Excel ===
columns_to_save = ['job_id', 'title', 'description', 'clean_description', 'has_description', 'description_word_count']
output_path = r'C:\Users\Sohyon\OneDrive\Desktop\Fake Job Listings\cleaned_description.xlsx'
df[columns_to_save].to_excel(output_path, index=False)

print(f"✅ Cleaned descriptions saved to: {output_path}")
