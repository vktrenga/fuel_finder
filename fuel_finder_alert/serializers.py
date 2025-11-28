from rest_framework import serializers
from .models import OpenCloseAlert, PriceDropAlert, StationAlertHistory

class StationAlertHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StationAlertHistory
        fields = "__all__"

class OpenCloseAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenCloseAlert
        fields = "__all__"
        read_only_fields = ("user","active",)

class PriceDropAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceDropAlert
        fields = "__all__"
        read_only_fields = ("user","active",)
