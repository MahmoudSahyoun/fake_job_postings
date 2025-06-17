import pandas as pd
from functools import reduce

# 1. Load the target label
base = pd.read_csv(
    "fake_job_postings.csv",
    usecols=["job_id", "fraudulent"]
)

# 2. Load all the feature tables
binary_flags       = pd.read_csv("binary_flags.csv")
onehot_structured  = pd.read_csv("onehot_structured.csv")
ordinal_features   = pd.read_csv("ordinal_features.csv")
parsed_location    = pd.read_csv("parsed_location.csv")
title_features     = pd.read_csv("title_features.csv")
# benefit_count lives in cleaned_title_benefits.csv
title_benefits     = pd.read_csv("cleaned_title_benefits.csv", usecols=["job_id","benefit_count"])
description_feat   = pd.read_csv("description_features.csv")
requirements_feat  = pd.read_csv("requirements_features_v2.csv")
company_profile_feat = pd.read_excel("company_profile_features.xlsx")

# 3. List of all DataFrames to merge
dfs = [
    base,
    binary_flags,
    onehot_structured,
    ordinal_features,
    parsed_location,
    title_features,
    title_benefits,
    description_feat,
    requirements_feat,
    company_profile_feat
]

# 4. Merge on job_id
model_df = reduce(
    lambda left, right: left.merge(right, on="job_id", how="left"),
    dfs
)

# 5. Save the combined dataset
model_df.to_csv("model_data.csv", index=False)
print(f"✅ model_data.csv created: {model_df.shape[0]} rows × {model_df.shape[1]} columns")
