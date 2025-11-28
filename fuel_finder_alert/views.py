from rest_framework import generics
from .models import OpenCloseAlert, PriceDropAlert, StationAlertHistory
from .serializers import OpenCloseAlertSerializer, PriceDropAlertSerializer, StationAlertHistorySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema


class StationAlertHistoryListView(generics.ListAPIView):
    serializer_class = StationAlertHistorySerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        queryset = StationAlertHistory.objects.filter(user=user)

        alert_type = self.request.query_params.get("alert_type")
        station = self.request.query_params.get("station")

        if alert_type:
            queryset = queryset.filter(alert_type=alert_type)
        if station:
            queryset = queryset.filter(station_id=station)

        return queryset
    
class OpenCloseAlertViews(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        request=OpenCloseAlertSerializer,
        responses=OpenCloseAlertSerializer
    )
    def post(self, request):
        """Update or create user open/close alert settings"""
        open_close_alert_setting, created = OpenCloseAlert.objects.get_or_create(user=request.user)

        serializer = OpenCloseAlertSerializer(
            open_close_alert_setting, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else :
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        responses=OpenCloseAlertSerializer
    )
    def get(self, request):
        open_close_alert_setting = OpenCloseAlert.objects.get(user=request.user)
        serializer = OpenCloseAlertSerializer(open_close_alert_setting)
        return Response(serializer.data, status=status.HTTP_200_OK)
     

class PriceDropAlertViews(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        request=PriceDropAlertSerializer,
        responses=PriceDropAlertSerializer
    )
    def post(self, request):
        """Update or create user Price Drop alert settings"""
        price_drop_alert_setting, created = PriceDropAlert.objects.get_or_create(user=request.user, fuel_type_id=request.data.get("fuel_type"))
        serializer = PriceDropAlertSerializer(
            price_drop_alert_setting, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        responses=PriceDropAlertSerializer(many=True)
    )
    def get(self, request):
        price_drop_alert_setting = PriceDropAlert.objects.filter(user=request.user)
        serializer = PriceDropAlertSerializer(price_drop_alert_setting, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)