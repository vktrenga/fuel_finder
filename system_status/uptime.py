import time

SERVICE_START_TIME = time.time()

def get_uptime():
    seconds = int(time.time() - SERVICE_START_TIME)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f"{hours}h {minutes}m"
