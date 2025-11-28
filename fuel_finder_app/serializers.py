from rest_framework import serializers

class PriceSerializer(serializers.Serializer):
    fuel_type = serializers.CharField()
    price_per_liter = serializers.FloatField()
    last_updated = serializers.DateTimeField()

class StationListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    city = serializers.CharField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    distance_km = serializers.FloatField(allow_null=True)
    is_open = serializers.BooleanField()
    price =  PriceSerializer(many=True)
    last_price_update = serializers.DateTimeField(allow_null=True)


class StationDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    address = serializers.CharField()
    city = serializers.CharField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    fuel_types = serializers.ListField(child=serializers.CharField())
    amenities = serializers.ListField(child=serializers.CharField())
    price =  PriceSerializer(many=True)
    price_history =  PriceSerializer(many=True)
    is_open = serializers.BooleanField()
    timings = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField())
    )

