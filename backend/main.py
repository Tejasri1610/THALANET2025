# main.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib

# Define request schema
class DonorInput(BaseModel):
    age: int
    blood_type: str
    location: str

# Initialize app
app = FastAPI()

# Load trained model (example: donor_model.pkl inside backend folder)
model = joblib.load("backend/donor_model.pkl")

@app.post("/predict")
def predict_donor(data: DonorInput):
    # Convert request into features
    features = [[data.age, 1 if data.blood_type == "O+" else 0, len(data.location)]]
    
    # Prediction
    prediction = model.predict(features)
    
    return {"prediction": str(prediction[0])}
