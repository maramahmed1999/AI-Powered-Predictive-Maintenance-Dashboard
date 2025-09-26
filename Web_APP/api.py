# api.py
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib
from tensorflow.keras.models import load_model

# Load model and scaler
model = load_model("lstm_rul_model_new.h5")
scaler = joblib.load("scaler_new.pkl")

app = FastAPI(title="Predictive Maintenance API")
SEQUENCE_LENGTH = 50

REQUIRED_FEATURES = [
    "op_setting_1", "op_setting_2",
    "sensor_2", "sensor_3", "sensor_4",
    "sensor_6", "sensor_7", "sensor_8", "sensor_9",
    "sensor_11", "sensor_12", "sensor_13", "sensor_14",
    "sensor_15", "sensor_17", "sensor_20", "sensor_21"
]

class SensorInput(BaseModel):
    engine_id: int
    readings: list

def preprocess_input(df: pd.DataFrame):
    missing_cols = [col for col in REQUIRED_FEATURES if col not in df.columns]
    if missing_cols:
        raise HTTPException(status_code=400, detail=f"Missing features: {missing_cols}")
    
    df = df[REQUIRED_FEATURES]
    df_scaled = scaler.transform(df)
    last_seq = df_scaled[-SEQUENCE_LENGTH:]
    
    if len(last_seq) < SEQUENCE_LENGTH:
        padded = np.zeros((SEQUENCE_LENGTH, len(REQUIRED_FEATURES)))
        padded[-len(last_seq):] = last_seq
        last_seq = padded
    
    return np.expand_dims(last_seq, axis=0)

@app.post("/predict/sensors")
async def predict_from_sensors(data: SensorInput):
    df = pd.DataFrame(data.readings)
    processed = preprocess_input(df)
    pred = model.predict(processed)
    return {"engine_id": data.engine_id, "predicted_RUL": float(pred[0][0])}

@app.post("/predict/file")
async def predict_file(file: UploadFile = File(...), engine_id: int = Form(...)):
    try:
        if file.filename.endswith(".txt"):
            df = pd.read_csv(file.file, sep=r"\s+", header=None)
            all_cols = ["engine_id", "cycle", "op_setting_1", "op_setting_2", "op_setting_3"] + [f"sensor_{i}" for i in range(1, df.shape[1]-5+1)]
            df.columns = all_cols[:df.shape[1]]
        else:
            df = pd.read_csv(file.file)

        missing_cols = [col for col in REQUIRED_FEATURES if col not in df.columns]
        if missing_cols:
            raise HTTPException(status_code=400, detail=f"Missing columns: {missing_cols}")

        X = df[REQUIRED_FEATURES]
        X_scaled = scaler.transform(X)

        if len(X_scaled) < SEQUENCE_LENGTH:
            padded = np.zeros((SEQUENCE_LENGTH, X_scaled.shape[1]))
            padded[-len(X_scaled):] = X_scaled
            X_scaled = padded
        else:
            X_scaled = X_scaled[-SEQUENCE_LENGTH:]

        X_scaled = np.expand_dims(X_scaled, axis=0)
        pred = model.predict(X_scaled)
        return {"engine_id": engine_id, "predicted_RUL": float(pred[0][0])}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")
