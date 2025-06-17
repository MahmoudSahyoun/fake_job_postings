import re
import pandas as pd
import lightgbm as lgb
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

# 1. Load final, imputed model data
df = pd.read_csv("model_data_final.csv")

# 2. Separate target & drop job_id
y = df["fraudulent"]
X = df.drop(columns=["fraudulent", "job_id"])

# 3. Keep only numeric/bool columns
X = X.select_dtypes(include=["number", "bool"])

# 4. Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 5. Sanitize column names
sanitized = [re.sub(r"[^0-9A-Za-z_]", "_", c) for c in X_train.columns]

# 6. Uniquify duplicates
unique_cols = []
counts = {}
for name in sanitized:
    if name not in counts:
        counts[name] = 0
        unique_cols.append(name)
    else:
        counts[name] += 1
        unique_cols.append(f"{name}_{counts[name]}")
X_train.columns = unique_cols
X_test.columns = unique_cols  # same renaming for test

# 7. Best params from your grid
best_params = {
    "colsample_bytree": 0.8,
    "learning_rate":    0.1,
    "max_depth":        -1,
    "n_estimators":     300,
    "num_leaves":       31,
    "subsample":        0.8,
    "objective":       "binary",
    "random_state":     42
}

# 8. Train final LightGBM
model = lgb.LGBMClassifier(**best_params)
model.fit(X_train, y_train)

# 9. Extract top-30 importances
imp = pd.Series(model.feature_importances_, index=X_train.columns)
top30 = imp.sort_values(ascending=False).head(30)

# 10. Plot
plt.figure(figsize=(8, 6))
top30.plot.barh()
plt.gca().invert_yaxis()
plt.title("Top 30 LightGBM Feature Importances")
plt.xlabel("Importance")
plt.tight_layout()
plt.show()
