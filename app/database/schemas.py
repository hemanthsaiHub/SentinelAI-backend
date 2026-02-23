from pydantic import BaseModel
from datetime import datetime
from typing import List

class MetricBase(BaseModel):
    cpu: float
    memory: float
    disk: float
    health_score: float

class MetricCreate(MetricBase):
    pass

class MetricResponse(MetricBase):
    id: int
    timestamp: datetime
    class Config:
        from_attributes = True

class AlertBase(BaseModel):
    message: str
    severity: str

class AlertResponse(AlertBase):
    id: int
    timestamp: datetime
    resolved: bool
    class Config:
        from_attributes = True
