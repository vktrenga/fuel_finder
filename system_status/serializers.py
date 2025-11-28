from rest_framework import serializers


class SystemStatusDataSerializer(serializers.Serializer):
    uptime = serializers.CharField()
    server_time = serializers.DateTimeField()

    memory_usage_mb = serializers.FloatField()
    cpu_usage_percent = serializers.FloatField()

    stations_count = serializers.IntegerField()
    alerts_count = serializers.IntegerField()
    db_status = serializers.CharField()

    last_price_update = serializers.DateTimeField(allow_null=True)
    last_open_close_update = serializers.DateTimeField(allow_null=True)

    rate_limit_usage = serializers.JSONField()
    requests_last_minute = serializers.IntegerField()

    version = serializers.CharField()
    