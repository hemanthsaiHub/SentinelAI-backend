from datetime import datetime, timedelta

def now_minus_hours(hours: int):
    return datetime.utcnow() - timedelta(hours=hours)

def format_timestamp(ts):
    return ts.strftime("%Y-%m-%d %H:%M:%S")
