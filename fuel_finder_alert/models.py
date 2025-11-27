from django.db import models
from django.contrib.auth.models import User

from fuel_finder_app.models import FuelStations, FuelTypes

class OpenCloseAlert(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    notify_on_open = models.BooleanField(default=True)
    notify_on_close = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    radius_km = models.FloatField(default=5.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.station.name}"
    
class PriceDropAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fuel_type = models.ForeignKey(FuelTypes, on_delete=models.CASCADE)
    target_price = models.DecimalField(max_digits=6, decimal_places=2)
    is_active = models.BooleanField(default=True)
    radius_km = models.FloatField(default=5.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'fuel_type')

    def __str__(self):
        return f"{self.user.username} - {self.station.name} - {self.fuel_type.name} < {self.target_price}"

class StationAlertHistory(models.Model):
    ALERT_TYPE_CHOICES = (
        ("price", "Price Alert"),
        ("open_close", "Open/Close Alert"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    station = models.ForeignKey(FuelStations, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPE_CHOICES)
    message = models.TextField()
    triggered_at = models.DateTimeField(auto_now_add=True)
    extra_data = models.JSONField(blank=True, null=True)  # Store any extra info like price, distance, etc.

    def __str__(self):
        return f"{self.user.username} | {self.station.name} | {self.alert_type}"