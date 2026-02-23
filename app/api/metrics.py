from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import psutil
from sqlalchemy import desc

from app.database.db import get_db
from app.database.models import Metric

router = APIRouter()

@router.get("/latest")
def get_latest_metrics(db: Session = Depends(get_db)):
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage('C:\\').percent
    health_score = max(0, 100 - (cpu * 0.4 + mem * 0.4 + disk * 0.2))
    
    metric = Metric(cpu=cpu, memory=mem, disk=disk, health_score=health_score)
    db.add(metric)
    db.commit()
    db.refresh(metric)
    return metric

@router.get("/history")
def get_history(limit: int = 50, db: Session = Depends(get_db)):
    metrics = db.query(Metric).order_by(desc(Metric.timestamp)).limit(limit).all()
    return metrics
