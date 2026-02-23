import psutil
from sqlalchemy.orm import Session
from ..database.db import get_db
from ..database.models import Metric

def collect_metrics(db: Session) -> Metric:
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage('C:\\').percent
    health_score = max(0, 100 - (cpu * 0.4 + mem * 0.4 + disk * 0.2))
    
    metric = Metric(cpu=cpu, memory=mem, disk=disk, health_score=health_score)
    db.add(metric)
    db.commit()
    db.refresh(metric)
    return metric

def check_alerts(db: Session, metric: Metric):
    alerts = []
    if metric.cpu > 90:
        alerts.append({"message": f"CRITICAL: CPU {metric.cpu:.1f}%", "severity": "CRITICAL"})
    elif metric.cpu > 80:
        alerts.append({"message": f"WARNING: High CPU {metric.cpu:.1f}%", "severity": "WARNING"})
    
    if metric.health_score < 40:
        alerts.append({"message": f"CRITICAL: Health {metric.health_score:.1f}", "severity": "CRITICAL"})
    
    for alert_data in alerts:
        from ..database.models import Alert
        alert = Alert(**alert_data)
        db.add(alert)
    db.commit()
    return alerts
