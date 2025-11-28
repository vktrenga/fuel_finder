from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from django.db.models import Prefetch, FloatField
from datetime import datetime
import math

from fuel_finder_auth_user.models import UserProfile
from .serializers import StationDetailSerializer, StationListSerializer
from .models import FuelStations,  FuelPrices
from django.db.models.expressions import RawSQL
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, OpenApiParameter

def check_is_open(station):
    now = datetime.now()
    weekday = now.weekday()

    timings = station.timings.filter(day_of_week=weekday).first()

    if not timings or not timings.open_time or not timings.close_time:
        return False

    now_time = now.time()

    return timings.open_time <= now_time <= timings.close_time

class StationDetailView(APIView):
    permission_classes = [AllowAny]
 
    def get(self, request, station_id):
        try:
            station = FuelStations.objects.select_related("city").prefetch_related(
                "fuel_types",
                "amenities",
                Prefetch("fuelprices_set", queryset=FuelPrices.objects.filter(is_active=True)),
                "timings",
            ).get(id=station_id)
        except FuelStations.DoesNotExist:
            return Response({"error": "Station not found"}, status=404)

        prices = [
            {
                "fuel_type": fp.fuel_type.name,
                "price_per_liter": float(fp.price_per_liter),
                "last_updated": fp.last_updated,
            }
            for fp in station.fuelprices_set.all()
        ]
        price_history = FuelPrices.objects.filter(fuel_station_id=station).order_by('-last_updated')
        price_history_detail = [
            {
                "fuel_type": fph.fuel_type.name,
                "price_per_liter": float(fph.price_per_liter),
                "last_updated": fph.last_updated,
            }
            for fph in price_history
        ]
        data = {
            "id": station.id,
            "name": station.name,
            "address": station.address,
            "city": station.city.name,
            "latitude": float(station.latitude),
            "longitude": float(station.longitude),
            "fuel_types": [ft.name for ft in station.fuel_types.all()],
            "amenities": [a.name for a in station.amenities.all()],
            "price": prices,
            "price_history": price_history_detail,
            "is_open": check_is_open(station),
            "timings": [
                {
                    "day_of_week": t.day_of_week,
                    "day_name": t.get_day_of_week_display(),
                    "open_time": str(t.open_time),
                    "close_time": str(t.close_time),
                }
                for t in station.timings.all()
            ]
        }

        serializer = StationDetailSerializer(data)
        return Response(serializer.data, status=200)

class StationListView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
    parameters=[
        OpenApiParameter(name='lat', type=float, location='query', description='User latitude'),
        OpenApiParameter(name='lng', type=float, location='query', description='User longitude'),
        OpenApiParameter(name='order', type=str, location='query', description='Order direction: asc or desc'),
        OpenApiParameter(name='order_by', type=str, location='query', description='Order by field: distance'),
        OpenApiParameter(name='fuel', type=str, location='query', description='Filter by fuel types, comma separated'),
        OpenApiParameter(name='min_price', type=float, location='query', description='Minimum price filter'),
        OpenApiParameter(name='max_price', type=float, location='query', description='Maximum price filter'),
        OpenApiParameter(name='city', type=str, location='query', description='Filter by city name'), 
        OpenApiParameter(name='city_id', type=int, location='query', description='Filter by city ID'),
        OpenApiParameter(name='is_open', type=str, location='query', description='Filter by open status: true or false'),    
    ],
    responses=StationDetailSerializer(many=True)
)
    def get(self, request):
        qs = (
            FuelStations.objects
            .select_related("city")
            .prefetch_related(
                "fuel_types",
                "amenities",
                Prefetch(
                    "fuelprices_set",
                    queryset=FuelPrices.objects.filter(is_active=True)
                        .order_by("-last_updated")
                ),
                "timings",
            )
        )

        # -------------------
        #  DISTANCE ORDERING
        # -------------------
        if request.user.is_authenticated:
            user_value = request.user
            user_profile = UserProfile.objects.get(user_id=user_value.id)
            user_lat = user_profile.latitude
            user_lng = user_profile.longitude
        else:
            user_lat = request.GET.get("lat")
            user_lng = request.GET.get("lng")

        if not user_lng or not user_lat:
            return Response({"detail": "Lat & Lng not present"}, status=400)       
         
        if user_lat and user_lng:
            user_lat = float(user_lat)
            user_lng = float(user_lng)

            haversine = """
                6371 * acos(
                    cos(radians(%s)) * cos(radians(fuel_finder_app_fuelstations.latitude)) *
                    cos(radians(fuel_finder_app_fuelstations.longitude) - radians(%s)) +
                    sin(radians(%s)) * sin(radians(fuel_finder_app_fuelstations.latitude))
                )
            """

            qs = qs.annotate(
                distance=RawSQL(
                    haversine,
                    (user_lat, user_lng, user_lat),
                    output_field=FloatField()
                )
            )
            order = request.GET.get("order")        # "asc" or "desc"
            order_by = request.GET.get("order_by")  # "distance"

            if order_by == "distance" and hasattr(qs[0], "distance"):
                if order == "desc":
                    qs = qs.order_by("-distance")
                else:  # default or "asc"
                    qs = qs.order_by("distance")
            elif order_by == None:
                qs = qs.order_by("distance")  # Default ordering

        # -------------------
        #  FILTERS
        # -------------------

        # Fuel type filter: ?fuel=Petrol,Diesel
        fuel_param = request.GET.get("fuel")
        if fuel_param:
            fuel_list = [f.strip() for f in fuel_param.split(",")]
            qs = qs.filter(fuel_types__name__in=fuel_list).distinct()

        #  Price filter: ?min_price=100&max_price=120
        min_price = request.GET.get("min_price")
        max_price = request.GET.get("max_price")

        if min_price:
            qs = qs.filter(fuelprices_set__price_per_liter__gte=min_price)
        if max_price:
            qs = qs.filter(fuelprices_set__price_per_liter__lte=max_price)

        if order_by == "price" and hasattr(qs[0], "price_per_liter"):
                if order == "desc":
                    qs = qs.order_by("-price_per_liter")
                else:  # default or "asc"
                    qs = qs.order_by("price_per_liter")
        #  City filters
        city = request.GET.get("city")
        city_id = request.GET.get("city_id")

        if city:
            qs = qs.filter(city__name__icontains=city)
        if city_id:
            qs = qs.filter(city__id=city_id)

        # Open / Closed filter: ?is_open=true
        is_open = request.GET.get("is_open")
        if is_open in ["true", "false"]:
            flag = is_open == "true"
            qs = [s for s in qs if check_is_open(s) == flag]

        # -------------------
        #  PAGINATION
        # -------------------
        paginator = PageNumberPagination()
        paginator.page_size = 10

        paginated_qs = paginator.paginate_queryset(qs, request)

        # -------------------
        #  Serialize Output
        # -------------------
        stations = []
        for s in paginated_qs:
            price_obj = s.fuelprices_set.first()

            stations.append({
                "id": s.id,
                "name": s.name,
                "city": s.city.name,
                "latitude": float(s.latitude),
                "longitude": float(s.longitude),
                "distance_km": round(s.distance, 2) if hasattr(s, "distance") else None,
                "is_open": check_is_open(s),
                "price": [
                    {
                        "fuel_type": fp.fuel_type.name,
                        "price_per_liter": float(fp.price_per_liter),
                        "last_updated": fp.last_updated,
                    }
                    for fp in s.fuelprices_set.all()
                ],
                "last_price_update": price_obj.last_updated if price_obj else None,
            })

        serializer = StationListSerializer(stations, many=True)
        return paginator.get_paginated_response(serializer.data)
