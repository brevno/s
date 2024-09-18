# server/periodic.py

from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
import time

app = FastAPI()

def periodic_task():
    print(f"Task executed at {time.strftime('%Y-%m-%d %H:%M:%S')}")

scheduler = BackgroundScheduler()
scheduler.add_job(periodic_task, 'interval', minutes=1)
scheduler.start()

@app.on_event("startup")
async def startup_event():
    scheduler.start()

@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()