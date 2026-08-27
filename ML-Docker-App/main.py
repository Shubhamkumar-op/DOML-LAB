from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

model = joblib.load("app/model.pkl")

class IrisFeatures(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

app = FastAPI(title="ML Model API")

@app.get("/")
def home():
    return {"message": "ML Model API is running"}

@app.post("/predict")
def predict(features: IrisFeatures):
    input_data = np.array([[
        features.sepal_length,
        features.sepal_width,
        features.petal_length,
        features.petal_width
    ]])

    prediction = model.predict(input_data)

    return {"prediction": int(prediction[0])}