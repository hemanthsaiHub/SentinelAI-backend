from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean
from sqlalchemy.sql import func
from .db import Base

class Metric(Base):
    __tablename__ = "metrics"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, server_default=func.now())
    cpu = Column(Float)
    memory = Column(Float)
    disk = Column(Float)
    health_score = Column(Float)

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, server_default=func.now())
    message = Column(String)
    severity = Column(String)  # INFO, WARNING, CRITICAL
    resolved = Column(Boolean, default=False)
