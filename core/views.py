import time
import psutil
from collections import deque

from django.db import connection
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response

from core.uptime import get_uptime
from fuel_finder_app.models import FuelStations
from fuel_finder_alert.models import StationAlertHistory

# Global request history for rate monitoring
REQUEST_HISTORY = deque(maxlen=5000)


class StatusView(APIView):
    authentication_classes = []   # optional
    permission_classes = []       # optional

    def initial(self, request, *args, **kwargs):
        # Track every request timestamp for global rate limit
        REQUEST_HISTORY.append(time.time())
        return super().initial(request, *args, **kwargs)

    def get(self, request):

        # CPU usage % (average over 0.5 sec)
        cpu_usage = psutil.cpu_percent(interval=0.5)

        # Memory usage
        process = psutil.Process()
        memory_mb = process.memory_info().rss / 1024 / 1024

        # DB status
        try:
            connection.cursor()
            db_status = "connected"
        except Exception:
            db_status = "not connected"

        # Last cron job (example: price update)
        price_history = StationAlertHistory.objects.filter(alert_type=StationAlertHistory.PRICE).order_by('-triggered_at').first()
        # Last cron job (example: price update)
        open_close_history = StationAlertHistory.objects.filter(alert_type__in=[StationAlertHistory.CLOSE, StationAlertHistory.OPEN]).order_by('-triggered_at').first()

        # Per-user rate limit usage (DRF throttle history)
        throttle_info = {}
        if request.user.is_authenticated:
            for throttle in self.get_throttles():
                scope = getattr(throttle, "scope", "default")
                history = getattr(throttle, "history", [])
                throttle_info[scope] = {
                    "requests_made": len(history),
                    "oldest_request": history[0] if history else None
                }

        # Global requests in last 60 seconds
        now_ts = time.time()
        requests_last_min = len([t for t in REQUEST_HISTORY if now_ts - t <= 60])

        data = {
            # System Info
            "uptime": get_uptime(),
            "server_time": now(),

            # Resource Stats
            "memory_usage_mb": round(memory_mb, 2),
            "cpu_usage_percent": cpu_usage,

            # App Data
            "stations_count": FuelStations.objects.count(),
            "alerts_count": StationAlertHistory.objects.count(),
            "db_status": db_status,

            # Cron Jobs
            "last_price_update": price_history.triggered_at if price_history else None,

            "last_open_close_update": open_close_history.triggered_at if open_close_history else None,

            # API Rate Information
            "rate_limit_usage": throttle_info,
            "requests_last_minute": requests_last_min,

            # Build / App Info
            "version": "v1.0.1"
        }

        return Response(data)
