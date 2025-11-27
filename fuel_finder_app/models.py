from django.db import models

# Create your models here.
class FuelTypes(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Amenities(models.Model):
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=200, null=True, blank=True, default="")
    def __str__(self):
        return self.name
    
class Cities(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class FuelStationTimings(models.Model):
    DAYS_OF_WEEK = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    fuel_station = models.ForeignKey('FuelStations', on_delete=models.CASCADE, related_name='timings')
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    open_time = models.TimeField(null=True, blank=True)
    close_time = models.TimeField(null=True, blank=True)
    class Meta:
        unique_together = ('fuel_station', 'day_of_week')
    def __str__(self):
        return f"{self.fuel_station.name} - {self.get_day_of_week_display()}: {self.open_time} to {self.close_time}"

class FuelStations(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    city = models.ForeignKey(Cities, on_delete=models.CASCADE)
    fuel_types = models.ManyToManyField(FuelTypes)
    amenities = models.ManyToManyField(Amenities, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.name
    
class FuelPrices(models.Model):
    fuel_station = models.ForeignKey(FuelStations, on_delete=models.CASCADE)
    fuel_type = models.ForeignKey(FuelTypes, on_delete=models.CASCADE)
    price_per_liter = models.DecimalField(max_digits=6, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            existing_active = FuelPrices.objects.filter(
                fuel_station=self.fuel_station,
                fuel_type=self.fuel_type,
                is_active=True)
            if not existing_active.exists():
                self.is_active = True
            else:
                FuelPrices.objects.filter(
                fuel_station=self.fuel_station,
                fuel_type=self.fuel_type,
                is_active=True).update(is_active=False)
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.fuel_station.name} - {self.fuel_type.name}: {self.price_per_liter} : {'Active' if self.is_active else 'Inactive'}"
    