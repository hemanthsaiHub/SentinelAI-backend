def check_rules(metric):
    alerts = []
    if metric.cpu > 90:
        alerts.append({"severity": "CRITICAL", "message": "High CPU usage"})
    if metric.health_score < 50:
        alerts.append({"severity": "WARNING", "message": "Low health score"})
    return alerts
