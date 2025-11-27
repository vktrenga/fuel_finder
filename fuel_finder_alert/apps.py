from django.apps import AppConfig


class FuelFinderAlertConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fuel_finder_alert'

    def ready(self):
        from . import scheduler
        scheduler.start()