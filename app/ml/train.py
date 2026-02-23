import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
from sqlalchemy.orm import Session
from ..database.models import Metric

def train_anomaly_model(db: Session):
    metrics = db.query(Metric).all()
    df = pd.DataFrame([(m.cpu, m.memory, m.disk) for m in metrics], 
                      columns=['cpu', 'memory', 'disk'])
    model = IsolationForest(contamination=0.1)
    model.fit(df)
    joblib.dump(model, 'backend/app/ml/models/anomaly_detector.pkl')
