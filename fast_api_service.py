from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, Dict
import pandas as pd
import joblib

# 1) Initialize FastAPI
app = FastAPI(
    title="Job Fraud Detection API",
    description="A RESTful API that predicts the probability of a job listing being fraudulent.",
    version="1.0",
)

# 2) Load model + feature list (created by train_lightgbm.py)
model = joblib.load("model.pkl")
feature_columns = joblib.load("feature_columns.pkl")  # must be a list[str]

# 3) Define a schema that accepts any feature key→value
class JobFeatures(BaseModel):
    """
    Any JSON keys are allowed here; they'll be interpreted as feature columns.
    """
    class Config:
        extra = "allow"  # accept arbitrary keys

@app.get("/health", tags=["Health"])
async def health_check():
    """Simple health check."""
    return {"status": "ok"}

@app.post("/predict", tags=["Prediction"])
async def predict_job_fraud(features: JobFeatures):
    """
    Accepts a JSON payload of feature_name: value pairs,
    returns the model's fraud probability.
    """
    # Convert the Pydantic model to a plain dict
    data: Dict[str, Any] = features.model_dump()

    # Build a 1-row DataFrame, reindex to exact feature list, missing→0
    df = pd.DataFrame([data])
    df = df.reindex(columns=feature_columns, fill_value=0)

    # Ensure correct dtypes for any bool cols (optional here)
    # df = df.astype({c: "int" for c in df.select_dtypes("boolean").columns})

    # Predict
    prob = model.predict_proba(df)[:, 1][0]
    return {"fraud_probability": float(prob)}

if __name__ == "__main__":
    # so you can do: python fast_api_service.py
    import uvicorn
    uvicorn.run("fast_api_service:app", host="127.0.0.1", port=8000, reload=True)
