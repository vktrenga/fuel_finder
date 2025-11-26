from django.contrib import admin

# Register your models here.
from .models import FuelPrices, FuelStationTimings, FuelTypes, Amenities, Cities, FuelStations
admin.site.register(FuelTypes)
admin.site.register(Amenities)
admin.site.register(Cities)
admin.site.register(FuelStations)
admin.site.register(FuelPrices)
admin.site.register(FuelStationTimings)