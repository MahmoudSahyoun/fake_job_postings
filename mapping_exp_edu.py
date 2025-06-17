import pandas as pd

# === 1. Load raw data ===
df = pd.read_csv("fake_job_postings.csv")

# === 2. Define ordinal mappings ===
exp_map = {
    "Internship": 0,
    "Entry level": 1,
    "Associate": 2,
    "Mid-Senior level": 3,
    "Director": 4,
    "Executive": 5,
    "Not Applicable": -1  # if you want to treat “Not Applicable” separately
}

edu_map = {
    "Unspecified": 0,
    "High School or equivalent": 1,
    "Associate": 2,
    "Bachelor's Degree": 3,
    "Master's Degree": 4,
    "PhD or equivalent": 5
}

# === 3. Apply mappings ===
df['req_exp_ordinal'] = df['required_experience'] \
    .map(exp_map) \
    .fillna(-1) \
    .astype(int)

df['req_edu_ordinal'] = df['required_education'] \
    .map(edu_map) \
    .fillna(0) \
    .astype(int)

# === 4. Save out the new features ===
out = df[[
    'job_id',
    'required_experience',
    'req_exp_ordinal',
    'required_education',
    'req_edu_ordinal'
]]

out.to_csv("ordinal_features.csv", index=False)
print("✅ ordinal_features.csv written with experience & education ordinals.")
