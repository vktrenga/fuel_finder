
from fuel_finder_app.scripts.cites import cities_list, create_superuser, random_coordinates
from  ..models import FuelTypes, Amenities, Cities, FuelStations, FuelPrices, FuelStationTimings
from django.utils import timezone
from random import choice, uniform, sample
import datetime

def run():
    create_superuser()
    # ----------------------
    # Fuel Types
    # ----------------------
    fuel_types_list = ['Petrol', 'Diesel', 'CNG', 'LPG']
    fuel_types = []
    for ft_name in fuel_types_list:
        ft, _ = FuelTypes.objects.get_or_create(name=ft_name)
        fuel_types.append(ft)

    # ----------------------
    # Amenities
    # ----------------------
    amenities_list = [
        {'name': 'Restroom', 'icon': 'restroom-icon.png'},
        {'name': 'Car Wash', 'icon': 'carwash-icon.png'},
        {'name': 'ATM', 'icon': 'atm-icon.png'},
        {'name': 'Food Court', 'icon': 'foodcourt-icon.png'},
    ]
    amenities = []
    for amenity in amenities_list:
        am, _ = Amenities.objects.get_or_create(name=amenity['name'], defaults={'icon': amenity['icon']})
        amenities.append(am)

    # ----------------------
    # Cities
    # ----------------------
    cities = []
    cities_data = cities_list()
    for city_row in cities_data:
        city, created = Cities.objects.get_or_create(
            name=city_row['city'],
            latitude=city_row['latitude'],
            longitude=city_row['longitude']
        )
        cities.append(city)
    # ----------------------
    # Fuel Stations
    # ----------------------
    for city in cities:
        for i in range(1, 6):  # 5 stations per city
            station_name = f"{city.name} Fuel Station {i}"
            lat, lon = random_coordinates(float(city.latitude), float(city.longitude), max_km=20)
            fs, created = FuelStations.objects.get_or_create(
                name=station_name,
                defaults={
                    'address': f"123 {station_name} Street",
                    'city': city,
                    'latitude':lat ,
                    'longitude': lon,
                }
            )
            # Randomly assign 1-3 fuel types
            fs.fuel_types.set(sample(fuel_types, k=choice([1, 2, 3])))

            # Randomly assign 0-3 amenities
            fs.amenities.set(sample(amenities, k=choice([0, 1, 2, 3])))

            fs.save()

            # ----------------------
            # Fuel Prices
            # ----------------------
            for ft in fs.fuel_types.all():
                FuelPrices.objects.create(
                    fuel_station=fs,
                    fuel_type=ft,
                    price_per_liter=round(uniform(80, 120), 2),  # random price
                    last_updated=timezone.now(),
                    is_active=True
                )

            # ----------------------
            # Fuel Station Timings (7 days)
            # ----------------------
            for day in range(7):
                open_hour = choice(range(5, 10))    # open between 5am-9am
                close_hour = choice(range(18, 24))  # close between 6pm-11pm
                open_time = datetime.time(hour=open_hour, minute=0)
                close_time = datetime.time(hour=close_hour, minute=0)
                FuelStationTimings.objects.get_or_create(
                    fuel_station=fs,
                    day_of_week=day,
                    defaults={
                        'open_time': open_time,
                        'close_time': close_time
                    }
                )
    print("Initial fuel stations, fuel types, amenities, prices, and timings created successfully!")
