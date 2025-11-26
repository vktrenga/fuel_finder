from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Prefetch, Q
from datetime import datetime
import math

from .models import FuelStations, FuelTypes, FuelPrices, FuelStationTimings

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # km

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)

    a = (math.sin(d_phi / 2) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

@api_view(["GET"])
def nearby_fuel_stations(request):
    try:
        user_lat = float(request.query_params.get("lat"))
        user_lon = float(request.query_params.get("lon"))
        radius_km = float(request.query_params.get("radius", 1000))  # default 10 km
    except:
        return Response({"error": "lat & lon are required"}, status=400)

    # Filters
    fuel_types = request.query_params.getlist("fuel_types")  # ?fuel_types=1&fuel_types=2
    min_price = request.query_params.get("min_price")
    max_price = request.query_params.get("max_price")
    is_open = request.query_params.get("is_open")
    order_by = request.query_params.get("order", "asc")  # asc/desc

    # ---------------------------------------
    # 1) Bounding Box Optimization (FAST)
    # ---------------------------------------
    lat_range = radius_km / 111  # 1 deg lat = 111km
    lon_range = radius_km / (111 * math.cos(math.radians(user_lat)))

    stations = FuelStations.objects.filter(
        latitude__gte=user_lat - lat_range,
        latitude__lte=user_lat + lat_range,
        longitude__gte=user_lon - lon_range,
        longitude__lte=user_lon + lon_range
    )

    # ---------------------------------------
    # 2) Heavy Prefetch Optimization
    # ---------------------------------------
    stations = stations.select_related("city").prefetch_related(
        "fuel_types",
        "amenities",
        Prefetch("fuelprices_set", queryset=FuelPrices.objects.filter(is_active=True)),
        "timings",
    )

    # ---------------------------------------
    # 3) Filter by Fuel Types
    # ---------------------------------------
    if fuel_types:
        stations = stations.filter(fuel_types__id__in=fuel_types).distinct()

    # ---------------------------------------
    # 4) Filter by Prices
    # ---------------------------------------
    if min_price:
        stations = stations.filter(fuelprices__price_per_liter__gte=min_price)

    if max_price:
        stations = stations.filter(fuelprices__price_per_liter__lte=max_price)

    # ---------------------------------------
    # 5) Filter by Open Now
    # ---------------------------------------
    if is_open in ["true", "false"]:
        now = datetime.now()
        weekday = now.weekday()
        stations = stations.filter(timings__day_of_week=weekday)

    # ---------------------------------------
    # 6) Calculate Distance for Remaining Stations
    # ---------------------------------------
    nearby = []

    for s in stations:
        distance = haversine_distance(user_lat, user_lon, float(s.latitude), float(s.longitude))

        if distance <= radius_km:
            price_obj = getattr(s, "fuelprices_set").first()

            nearby.append({
                "id": s.id,
                "name": s.name,
                "address": s.address,
                "city": s.city.name,
                "latitude": float(s.latitude),
                "longitude": float(s.longitude),
                "distance_km": round(distance, 2),
                "fuel_types": [ft.name for ft in s.fuel_types.all()],
                "amenities": [a.name for a in s.amenities.all()],
                "price": float(price_obj.price_per_liter) if price_obj else None,
                "is_open": check_is_open(s),
            })

    # ---------------------------------------
    # 7) Order (distance asc/desc)
    # ---------------------------------------
    nearby.sort(key=lambda x: x["distance_km"], reverse=(order_by == "desc"))

    # ---------------------------------------
    # 8) Pagination
    # ---------------------------------------
    paginator = PageNumberPagination()
    paginator.page_size = 10
    result_page = paginator.paginate_queryset(nearby, request)

    return paginator.get_paginated_response(result_page)

def check_is_open(station):
    now = datetime.now()
    weekday = now.weekday()

    timings = station.timings.filter(day_of_week=weekday).first()

    if not timings or not timings.open_time or not timings.close_time:
        return False

    now_time = now.time()

    return timings.open_time <= now_time <= timings.close_time