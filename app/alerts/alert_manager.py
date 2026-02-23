from ..database.db import get_db
from ..database.models import Alert
from ..database.schemas import AlertBase
from ..monitoring.metrics import collect_metrics
from .rules import check_rules
from .notifier import send_notification
from sqlalchemy.orm import Session

def process_alerts(db: Session):
    metric = collect_metrics(db)
    rule_alerts = check_rules(metric)
    for alert_data in rule_alerts:
        alert = Alert(**alert_data)
        db.add(alert)
        send_notification(alert_data)
    db.commit()
