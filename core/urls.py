from django.urls import path
from core.views import StatusView
urlpatterns = [
    path("status/", StatusView.as_view(), name="status"),
]
