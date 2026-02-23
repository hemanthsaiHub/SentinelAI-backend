# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psutil
from datetime import datetime
import sqlite3
import threading
import time
import uvicorn

app = FastAPI(title="SentinelAI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Create or open database ----
conn = sqlite3.connect('sentinelai.db', check_same_thread=False)
cursor = conn.cursor()

# ---- Ensure tables exist with id column ----
cursor.execute('''
CREATE TABLE IF NOT EXISTS metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    cpu REAL,
    memory REAL,
    disk REAL,
    health REAL
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    message TEXT,
    severity TEXT
)
''')
conn.commit()


def save_metrics_periodically(interval: int = 5):
    """Background thread to save metrics every `interval` seconds."""
    while True:
        try:
            cpu = psutil.cpu_percent(interval=0.5)
            mem = psutil.virtual_memory().percent
            disk = psutil.disk_usage('C:\\').percent if 'C:\\' else 0
            health = max(0, 100 - (cpu * 0.4 + mem * 0.4 + disk * 0.2))

            # Save metric
            cursor.execute(
                "INSERT INTO metrics (timestamp, cpu, memory, disk, health) VALUES (?, ?, ?, ?, ?)",
                (datetime.now().isoformat(), cpu, mem, disk, health)
            )
            conn.commit()

            # Trigger alert
            if cpu > 90:
                msg = f"CRITICAL: CPU {cpu:.1f}%"
                cursor.execute(
                    "INSERT INTO alerts (timestamp, message, severity) VALUES (?, ?, ?)",
                    (datetime.now().isoformat(), msg, "CRITICAL")
                )
                conn.commit()

            time.sleep(interval)
        except Exception as e:
            print("Background thread error:", e)
            time.sleep(interval)


# Start background thread AFTER tables are ready
threading.Thread(target=save_metrics_periodically, daemon=True).start()


# ---- Endpoints ----
@app.get("/")
async def root():
    try:
        cursor.execute("SELECT * FROM metrics ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        latest_metric = {
            "timestamp": row[1], "cpu": row[2], "memory": row[3],
            "disk": row[4], "health": row[5]
        } if row else {}

        cursor.execute("SELECT * FROM alerts ORDER BY id DESC LIMIT 5")
        alerts_rows = cursor.fetchall()
        alerts = [{"timestamp": r[1], "message": r[2], "severity": r[3]} for r in alerts_rows]

        status = "HEALTHY"
        if latest_metric:
            if latest_metric["health"] <= 40:
                status = "CRITICAL"
            elif latest_metric["health"] <= 70:
                status = "WARNING"

        return {
            "message": "SentinelAI LIVE! 🚀",
            "latest_metric": latest_metric,
            "status": status,
            "alerts": alerts
        }
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/metrics/latest")
async def latest_metrics():
    try:
        cursor.execute("SELECT * FROM metrics ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        if row:
            return {"timestamp": row[1], "cpu": row[2], "memory": row[3], "disk": row[4], "health": row[5]}
        return {"message": "No metrics found yet."}
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/metrics/history")
async def metrics_history(limit: int = 50):
    try:
        cursor.execute(f"SELECT * FROM metrics ORDER BY id DESC LIMIT {limit}")
        rows = cursor.fetchall()
        if not rows:
            return {"message": "No metrics history found."}
        return [{"timestamp": r[1], "cpu": r[2], "memory": r[3], "disk": r[4], "health": r[5]} for r in rows]
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/alerts")
async def get_alerts(limit: int = 20):
    try:
        cursor.execute(f"SELECT * FROM alerts ORDER BY id DESC LIMIT {limit}")
        rows = cursor.fetchall()
        if not rows:
            return {"message": "No alerts found."}
        return [{"timestamp": r[1], "message": r[2], "severity": r[3]} for r in rows]
    except Exception as e:
        return {"error": str(e)}


@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)