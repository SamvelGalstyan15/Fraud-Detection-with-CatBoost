import json
import pandas as pd
from catboost import CatBoostClassifier
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

model = CatBoostClassifier()
model.load_model("fraud_catboost_model.cbm")

class Transaction(BaseModel):
    step: int
    type: str
    amount: float
    oldbalanceOrg: float
    newbalanceOrig: float
    oldbalanceDest: float
    newbalanceDest: float

@app.post("/predict")
def predict_fraud(data: Transaction):
    try:
        input_data = pd.DataFrame([data.model_dump()])
        proba = float(model.predict_proba(input_data)[0, 1])
        is_fraud = 1 if proba >= 0.0943 else 0
          
        return {
            "status": "success",
            "verdict": "BLOCK" if is_fraud == 1 else "ALLOW",
            "fraud_probability": round(proba, 6),
            "threshold_applied": 0.0943,
        }
    except Exception as ex:
        return {
            'Status': 'Error',
            'Error_type': type(ex).__name__,
            'Message' : str(ex)
        }
if __name__ == '__main__':
    uvicorn.run('predict:app', host='0.0.0.0', port=8000)

    
