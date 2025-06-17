import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
from sklearn.metrics import roc_auc_score
import lightgbm as lgb
import joblib   # ← add this import

# 1) Load your final model‐ready data
df = pd.read_csv("model_data_final.csv")

# 2) Define target and drop truly non‐numeric columns
y = df["fraudulent"]
X = df.drop(columns=[
    "job_id",
    "fraudulent",
    # drop any object columns you no longer need
    "required_experience",
    "required_education",
    "location",
    "country",
    "state",
    "city",
])

# 3) Convert bool → int and keep only numeric
for c in X.select_dtypes(include="bool"):
    X[c] = X[c].astype(int)
X = X.select_dtypes(include=["int64", "float64"])

# 4) Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# 5) Set up LightGBM + hyperparameter grid
clf = lgb.LGBMClassifier(objective="binary", metric="auc", random_state=42)

param_grid = {
    "n_estimators": [100, 300, 500],
    "learning_rate": [0.01, 0.1],
    "max_depth": [10, 20, -1],
    "num_leaves": [31, 127],
    "subsample": [0.8, 1.0],
    "colsample_bytree": [0.8, 1.0],
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
grid = GridSearchCV(
    clf,
    param_grid,
    scoring="roc_auc",
    cv=cv,
    n_jobs=-1,
    verbose=2,
    error_score="raise"   # so we see any actual fit errors immediately
)

# 6) Fit & report
grid.fit(X_train, y_train)
print("BEST PARAMS:", grid.best_params_)
print("CV AUC:", grid.best_score_)

# 7) Final evaluation on hold‐out test set
best = grid.best_estimator_
y_pred = best.predict_proba(X_test)[:, 1]
print("TEST SET AUC:", roc_auc_score(y_test, y_pred))

# ───────────────────────────────────────────────────────────────────────────────
# 8) Dump model + feature‐list for your FastAPI service:
# ───────────────────────────────────────────────────────────────────────────────
# Save the model
joblib.dump(best, "model.pkl")
print("✅ Model saved to model.pkl")

# Save the ordered list of feature‐columns your service will need
feature_columns = list(X_train.columns)
joblib.dump(feature_columns, "feature_columns.pkl")
print("✅ Feature list saved to feature_columns.pkl")
