from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class PredictionRequest(BaseModel):
    cpu: float
    memory: float
    disk: float

@router.post("/anomaly")
def predict_anomaly(data: PredictionRequest):
    # Simple anomaly detection
    health = 100 - (data.cpu * 0.4 + data.memory * 0.4 + data.disk * 0.2)
    is_anomaly = health < 30
    return {"prediction": "ANOMALY" if is_anomaly else "NORMAL", "health": health}
