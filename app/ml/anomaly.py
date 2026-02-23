# Isolation Forest for unsupervised anomaly detection
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import pandas as pd
import joblib
from ..database.db import get_db

def detect_anomalies_recent(hours: int = 24):
    db = next(get_db())
    # Fetch recent metrics, detect outliers
    scaler = StandardScaler()
    model = IsolationForest()
    # Train/predict logic similar to train.py
    return anomalies_list
