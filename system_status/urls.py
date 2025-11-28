from django.urls import path
from system_status.views import StatusView
urlpatterns = [
    path("status/", StatusView.as_view(), name="status"),
]
