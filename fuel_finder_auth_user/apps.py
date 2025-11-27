from django.apps import AppConfig


class FuelFinderAuthUserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fuel_finder_auth_user'
    def ready(self):
        import fuel_finder_auth_user.signals