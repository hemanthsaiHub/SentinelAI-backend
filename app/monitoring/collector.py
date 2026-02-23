import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ..database.db import get_db
from ..alerts.alert_manager import process_alerts
from ..core.logger import logger

scheduler = AsyncIOScheduler()

async def start_collector():
    scheduler.add_job(process_alerts, 'interval', seconds=30, args=(next(get_db()),))
    scheduler.start()
    logger.info("Metrics collector started")

# Call in main.py lifespan
