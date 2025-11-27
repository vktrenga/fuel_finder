from django.urls import path
from .views import  StationAlertHistoryListView
urlpatterns = [
    path('list/', StationAlertHistoryListView.as_view(), name='alert-list'),
]
