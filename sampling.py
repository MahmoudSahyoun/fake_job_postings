# impute_ordinals.py

import pandas as pd

# 1. Load the partially imputed data
df = pd.read_csv("model_data_imputed.csv")

# 2. Fill missing ordinals with 0 (“Not Specified”)
df["req_exp_ordinal"] = df["req_exp_ordinal"].fillna(0).astype(int)
df["req_edu_ordinal"] = df["req_edu_ordinal"].fillna(0).astype(int)

# 3. (Optional) sanity-check no more NaNs in those columns
print("Remaining missing in req_exp_ordinal:", df["req_exp_ordinal"].isna().sum())
print("Remaining missing in req_edu_ordinal:", df["req_edu_ordinal"].isna().sum())

# 4. Save the fully imputed dataset
df.to_csv("model_data_final.csv", index=False)
print("✅ Written model_data_final.csv with all ordinals imputed.")
