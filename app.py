import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

# Load the LightGBM model
model = joblib.load('lgb_model.pkl')

# Create FastAPI instance
app = FastAPI()

# Define the request model using Pydantic
class PremiumPrediction(BaseModel):
    age: int
    gender: str
    marital_status: str
    occupation: str
    vehicle_age: int
    vehicle: str
    property_value: int
    zip_code: str
    claim_history: str
    coverage_type: str

# Define the prediction endpoint
@app.post("/predict/")
def predict(request: PremiumPrediction):
    # Convert the incoming data into a DataFrame
    input_data = pd.DataFrame([{
        "age": request.age,
        "gender": request.gender,
        "marital_status": request.marital_status,
        "occupation": request.occupation,
        "vehicle_age": request.vehicle_age,
        "vehicle": request.vehicle,
        "property_value": request.property_value,
        "zip_code": request.zip_code,
        "claim_history": request.claim_history,
        "coverage_type": request.coverage_type,
    }])
    
    # Convert categorical columns to 'category' dtype if needed
    categorical_columns = ['gender', 'marital_status', 'occupation', 'vehicle', 'zip_code', 'claim_history', 'coverage_type']
    for col in categorical_columns:
        input_data[col] = input_data[col].astype('category')
    
    # Make the prediction
    prediction = model.predict(input_data)
    
    # Return the prediction as a response
    return {"prediction": prediction[0]}
