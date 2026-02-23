# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psutil
from datetime import datetime
import sqlite3
import uvicorn

app = FastAPI(title="SentinelAI Backend")

# Allow all origins for testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SQLite database
conn = sqlite3.connect('sentinelai.db', check_same_thread=False)
cursor = conn.cursor()

# Create tables
cursor.execute('''CREATE TABLE IF NOT EXISTS metrics 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   timestamp TEXT, cpu REAL, memory REAL, disk REAL, health REAL)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS alerts 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   timestamp TEXT, message TEXT, severity TEXT)''')
conn.commit()

@app.get("/")
async def root():
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage('C:\\').percent if 'C:\\' else 0
    health = max(0, 100 - (cpu*0.4 + mem*0.4 + disk*0.2))

    # Save metrics
    cursor.execute("INSERT INTO metrics (timestamp, cpu, memory, disk, health) VALUES (?, ?, ?, ?, ?)",
                  (datetime.now().isoformat(), cpu, mem, disk, health))
    conn.commit()

    # Alerts
    alerts = []
    if cpu > 90:
        msg = f"CRITICAL: CPU {cpu:.1f}%"
        cursor.execute("INSERT INTO alerts (timestamp, message, severity) VALUES (?, ?, ?)",
                      (datetime.now().isoformat(), msg, "CRITICAL"))
        conn.commit()
        alerts.append({"message": msg, "severity": "CRITICAL"})

    return {
        "message": "SentinelAI LIVE! 🚀",
        "cpu": round(cpu, 1),
        "memory": round(mem, 1),
        "disk": round(disk, 1),
        "health": round(health, 1),
        "status": "HEALTHY" if health > 70 else "WARNING" if health > 40 else "CRITICAL",
        "alerts": alerts
    }

@app.get("/api/metrics/latest")
async def latest_metrics():
    cursor.execute("SELECT * FROM metrics ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    if row:
        return {"timestamp": row[1], "cpu": row[2], "memory": row[3], "disk": row[4], "health": row[5]}
    return {}

@app.get("/api/metrics/history")
async def metrics_history(limit: int = 50):
    cursor.execute(f"SELECT * FROM metrics ORDER BY id DESC LIMIT {limit}")
    rows = cursor.fetchall()
    return [{"timestamp": r[1], "cpu": r[2], "memory": r[3], "disk": r[4], "health": r[5]} for r in rows]

@app.get("/api/alerts")
async def get_alerts(limit: int = 20):
    cursor.execute(f"SELECT * FROM alerts ORDER BY id DESC LIMIT {limit}")
    rows = cursor.fetchall()
    return [{"timestamp": r[1], "message": r[2], "severity": r[3]} for r in rows]

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)