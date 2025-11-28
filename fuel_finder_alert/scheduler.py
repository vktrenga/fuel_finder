from apscheduler.schedulers.background import BackgroundScheduler
from .cron import generate_open_close_alerts, generate_price_drop_alerts
from datetime import datetime, timedelta

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(generate_open_close_alerts, 'interval', minutes=30,
    next_run_time=datetime.now() + timedelta(minutes=5))
    scheduler.add_job(generate_price_drop_alerts, 'interval', 
    minutes=30,  next_run_time=datetime.now() + timedelta(minutes=5))
    scheduler.start()
