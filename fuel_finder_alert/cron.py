from django.utils import timezone
from datetime import datetime

from fuel_finder_app.models import FuelPrices, FuelStationTimings, FuelStations
from fuel_finder_auth_user.models import UserProfile
from .models import PriceDropAlert, StationAlertHistory, OpenCloseAlert
from django.contrib.auth import get_user_model
import math

User = get_user_model()

def calculate_distance_km(lat1, lon1, lat2, lon2):
    R = 6371
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)

    a = (math.sin(d_lat / 2) ** 2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(d_lon / 2) ** 2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

# Generate Open/Close Alerts
'''
Fetch the fuel station timings for the current day.
Check if the current time falls within the open and close times.
If there's a change in status (open to close or close to open), update the station status.
For each user, calculate the distance to the station. 
If within the alert radius, create an alert history entry.
'''
def generate_open_close_alerts():
    print("CRON executed...generate_open_close_alerts")
    now = timezone.localtime()
    day = now.weekday()

    timings = FuelStationTimings.objects.filter(day_of_week=day).order_by('-last_updated')[:10]
    for timing in timings:
        station = timing.fuel_station
        open_t = timing.open_time
        close_t = timing.close_time
        if not open_t or not close_t:
            continue

        # now is timezone-aware
        current_time = now.time()  # naive time object
        is_open_now = timing.open_time <= current_time <= timing.close_time
        if is_open_now != timing.is_open:
            print("Status changed for station:", station.name)
            continue

        userProfiles = UserProfile.objects.all()
        
        for userProfile in userProfiles:
            if not userProfile.latitude or not userProfile.longitude:
                continue

            distance = calculate_distance_km(
                userProfile.latitude,
                userProfile.longitude,
                station.latitude,
                station.longitude
            )
            getUserAlerts = OpenCloseAlert.objects.filter(user=userProfile.user, is_active=True)
            if not getUserAlerts.exists():
                continue
            # Alert only for users within 20 km
            if distance <= getUserAlerts.first().radius_km:
                status = "Close"
                print("radius_km", getUserAlerts.first().radius_km)
                if is_open_now  and getUserAlerts.first().notify_on_open:
                    status = "Open"
                if not is_open_now and getUserAlerts.first().notify_on_close:
                    status = "Close"
                # Insert alert history
                alert = StationAlertHistory.objects.create(
                    user=userProfile.user,
                    station=station,
                    alert_type=status,
                    triggered_at=now,
                    message=f"Station {station.name} is now {status}. Distance: {round(distance, 2)} km"
                )
                print("StationAlertHistory working", alert)

        timing.is_open = is_open_now
        timing.last_updated = now
        timing.save()

# Generate Price Drop Alerts
'''
Fetch recent fuel prices.  
For each price, find users with active price drop alerts for that fuel type.
For each user, calculate the distance to the station.  
If within the alert radius and the price is below the target, create an alert history entry.
'''
def generate_price_drop_alerts():
    print("CRON executed...generate_price_drop_alerts")
    now = timezone.localtime()
    day = now.weekday()

    fuel_prices = FuelPrices.objects.filter(is_active=True).order_by('-last_updated')[:10]
    for fuel_price in fuel_prices:
        station = fuel_price.fuel_station
        fuel_type = fuel_price.fuel_type   
        user_price_alerts = PriceDropAlert.objects.filter(is_active=True, fuel_type=fuel_type)
        for user_price_alert in user_price_alerts:
            userProfile = UserProfile.objects.filter(user=user_price_alert.user).first()
            if not userProfile or not userProfile.latitude or not userProfile.longitude:
                continue

            distance = calculate_distance_km(
                userProfile.latitude,
                userProfile.longitude,
                station.latitude,
                station.longitude
            )
           
            # Alert only for users within 20 km
            if distance <= user_price_alert.radius_km and fuel_price.price_per_liter <= user_price_alert.target_price:
                status = "Price Drop"
                # Insert alert history
                alert = StationAlertHistory.objects.create(
                    user=userProfile.user,
                    station=station,
                    alert_type=status,
                    triggered_at=now,
                    message=f" The price of {fuel_type} is droped to {fuel_price.price_per_liter} at station {station.name}. Distance: {round(distance, 2)} km"
                )
                print("StationAlertHistory working", alert)