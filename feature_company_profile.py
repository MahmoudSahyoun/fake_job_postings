import pandas as pd
import re

# === 1. Load cleaned company profiles ===
clean_path = "cleaned_company_profile.xlsx"
df_clean = pd.read_excel(clean_path)

# Make a copy for features
df = df_clean.copy()

# === 2. Basic text-stats features ===
# Word count
df['company_profile_word_count'] = df['clean_company_profile'] \
    .fillna("") \
    .apply(lambda txt: len(str(txt).split()))

# Character count
df['company_profile_char_count'] = df['clean_company_profile'] \
    .fillna("") \
    .apply(lambda txt: len(str(txt)))

# Average word length
df['company_profile_avg_word_length'] = df['clean_company_profile'] \
    .fillna("") \
    .apply(lambda txt: sum(len(w) for w in str(txt).split()) / max(len(str(txt).split()), 1))

# Sentence count (approximate by punctuation)
df['company_profile_num_sentences'] = df['clean_company_profile'] \
    .fillna("") \
    .apply(lambda txt: sum(txt.count(c) for c in ".!?"))

# === 3. Keyword flags ===
keywords = {
    'inc':      r'\binc\b',
    'llc':      r'\bllc\b',
    'ltd':      r'\bltd\b',
    'startup':  r'\bstartup\b',
    'global':   r'\bglobal\b',
}

for key, pat in keywords.items():
    df[f'company_profile_has_{key}'] = df['clean_company_profile'] \
        .str.contains(pat, case=False, na=False).astype(int)

# === 4. Extract & save just the feature columns ===
feature_cols = [
    'job_id',
    'company_profile_word_count',
    'company_profile_char_count',
    'company_profile_avg_word_length',
    'company_profile_num_sentences',
] + [f'company_profile_has_{k}' for k in keywords]

df[feature_cols].to_excel("company_profile_features.xlsx", index=False)

# === 5. Merge features back into the cleaned profiles ===
feat_df = pd.read_excel("company_profile_features.xlsx")
merged = df_clean.merge(feat_df, on="job_id", how="left")

# === 6. Save the merged file ===
merged.to_excel("cleaned_company_profile_with_features.xlsx", index=False)
print("✅ cleaned_company_profile_with_features.xlsx generated with all profile features.")
