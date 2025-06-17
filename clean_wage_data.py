import pandas as pd
import numpy as np

# === 1. Load the Dataset ===
file_path = r'C:\Users\Sohyon\OneDrive\Desktop\Fake Job Listings\fake_job_postings.csv'
df = pd.read_csv(file_path)

# === 2. Add a Binary Flag for Missing Salary ===
df['missing_salary'] = df['salary_range'].isnull().astype(int)

# === 3. Extract min_salary and max_salary from salary_range ===
def extract_min_max(s):
    try:
        if pd.isnull(s):
            return np.nan, np.nan
        if '-' in s:
            parts = s.split('-')
            return int(parts[0]), int(parts[1])
        else:
            val = int(s)
            return val, val
    except:
        return np.nan, np.nan

df[['min_salary', 'max_salary']] = df['salary_range'].apply(
    lambda x: pd.Series(extract_min_max(x))
)

# === 4. Group Median Salaries by Title for Imputation ===
median_salaries = df.groupby('title')[['min_salary', 'max_salary']].median()

def fill_salary_by_title(row):
    if pd.isnull(row['min_salary']) or pd.isnull(row['max_salary']):
        title = row['title']
        if title in median_salaries.index:
            med = median_salaries.loc[title]
            return pd.Series([med['min_salary'], med['max_salary']])
    return pd.Series([row['min_salary'], row['max_salary']])

df[['min_salary', 'max_salary']] = df.apply(fill_salary_by_title, axis=1)

# === 5. Create Mean Salary Column ===
df['mean_salary'] = df[['min_salary', 'max_salary']].mean(axis=1)

# === 6. Save only selected columns to a new Excel file ===
output_columns = ['title', 'salary_range', 'missing_salary', 'min_salary', 'max_salary', 'mean_salary']
output_path = r'C:\Users\Sohyon\OneDrive\Desktop\Fake Job Listings\salary_analysis_output.xlsx'
df[output_columns].to_excel(output_path, index=False)

# === 7. Confirm Save ===
print(f"✅ Saved: {output_path}")
