from apscheduler.schedulers.background import BackgroundScheduler
from .cron import generate_open_close_alerts, generate_price_drop_alerts

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(generate_open_close_alerts, 'interval', seconds=10)
    scheduler.add_job(generate_price_drop_alerts, 'interval', seconds=5)
    scheduler.start()
