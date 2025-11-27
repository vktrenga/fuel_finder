from rest_framework import generics
from .models import StationAlertHistory
from .serializers import StationAlertHistorySerializer
from rest_framework.permissions import IsAuthenticated

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
