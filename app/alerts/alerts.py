from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...database.db import get_db
from ...database.schemas import AlertResponse
from ...database.models import Alert
from ...alerts.alert_manager import process_alerts

router = APIRouter()

@router.get("/", response_model=list[AlertResponse])
def get_alerts(db: Session = Depends(get_db)):
    return db.query(Alert).order_by(Alert.timestamp.desc()).limit(50).all()

@router.post("/trigger")
def trigger_alert():
    process_alerts(next(get_db()))
    return {"status": "alerts processed"}
