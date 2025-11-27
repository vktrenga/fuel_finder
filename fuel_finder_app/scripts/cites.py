import random
import math
from django.contrib.auth import get_user_model
User = get_user_model()

def cities_list():
    return [
            {"city": "Chennai", "latitude": 13.08998781, "longitude": 80.27999874},
            {"city": "Coimbatore", "latitude": 10.99996035, "longitude": 76.95002112},
            {"city": "Cuddalore", "latitude": 11.72040733, "longitude": 79.77000403},
            {"city": "Dindigul", "latitude": 10.37997235, "longitude": 78.00003454},
            {"city": "Kanchipuram", "latitude": 12.83372438, "longitude": 79.71667395},
            {"city": "Karur", "latitude": 10.95037681, "longitude": 78.08333695},
            {"city": "Kumbakonam", "latitude": 10.98047833, "longitude": 79.40000077},
            {"city": "Madurai", "latitude": 9.920026264, "longitude": 78.12002722},
            {"city": "Nagercoil", "latitude": 8.180365009, "longitude": 77.42999182},
            {"city": "Rajapalaiyam", "latitude": 9.420392679, "longitude": 77.5800085},
            {"city": "Salem", "latitude": 11.66999697, "longitude": 78.18007523},
            {"city": "Thanjavur", "latitude": 10.77041363, "longitude": 79.15004187},
            {"city": "Tiruchirappalli", "latitude": 10.80999778, "longitude": 78.68996659},
            {"city": "Tirunelveli", "latitude": 8.730408955, "longitude": 77.68997595},
            {"city": "Tiruppur", "latitude": 11.08042055, "longitude": 77.32999792},
            {"city": "Tiruvannamalai", "latitude": 12.26037437, "longitude": 79.09996741},
            {"city": "Tuticorin", "latitude": 8.81999005, "longitude": 78.13000077},
            {"city": "Valparai", "latitude": 10.32041526, "longitude": 76.96996822},
            {"city": "Vellore", "latitude": 12.92038576, "longitude": 79.15004187}
    ]

def random_coordinates(lat, lon, max_km=30):
    """
    Returns a random latitude and longitude within `max_km` km of the original coordinates.
    """
    # Earth's radius in km
    R = 6371

    # Random distance in km
    distance = random.uniform(0, max_km)

    # Random bearing in radians
    bearing = random.uniform(0, 2 * math.pi)

    # Original coordinates in radians
    lat1 = math.radians(lat)
    lon1 = math.radians(lon)

    # New latitude in radians
    lat2 = math.asin(math.sin(lat1) * math.cos(distance / R) +
                     math.cos(lat1) * math.sin(distance / R) * math.cos(bearing))

    # New longitude in radians
    lon2 = lon1 + math.atan2(math.sin(bearing) * math.sin(distance / R) * math.cos(lat1),
                             math.cos(distance / R) - math.sin(lat1) * math.sin(lat2))

    # Convert back to degrees
    return round(math.degrees(lat2), 6), round(math.degrees(lon2), 6)

def create_superuser():
    User = get_user_model()
    superuser_data = {
        'username': 'admin',
        'email': 'admin@example.com',
        'is_staff': True,
        'is_superuser': True,
        'password': 'admin123',
    }
    user, created = User.objects.get_or_create(username=superuser_data['username'], defaults=superuser_data)
    if created:
        user.set_password('admin123')  # Set your default password
        user.save()
        print("Superuser created: admin / admin123")
    else:
        print("Superuser already exists: admin")
