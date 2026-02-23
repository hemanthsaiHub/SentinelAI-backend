from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from ...database.db import get_db
from ...database.models import Alert

router = APIRouter()

@router.get("/")
def get_alerts(limit: int = 20, db: Session = Depends(get_db)):
    alerts = db.query(Alert).order_by(desc(Alert.timestamp)).limit(limit).all()
    return alerts
