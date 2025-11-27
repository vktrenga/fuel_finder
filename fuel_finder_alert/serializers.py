from rest_framework import serializers
from .models import StationAlertHistory

class StationAlertHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StationAlertHistory
        fields = "__all__"
