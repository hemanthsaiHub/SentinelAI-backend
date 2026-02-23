import joblib
import numpy as np

model = joblib.load('backend/app/ml/models/anomaly_detector.pkl')

def predict_anomaly(cpu: float, mem: float, disk: float) -> str:
    pred = model.predict(np.array([[cpu, mem, disk]]))[0]
    return "ANOMALY" if pred == -1 else "NORMAL"
