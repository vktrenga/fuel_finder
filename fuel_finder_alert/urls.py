from django.urls import path
from .views import  OpenCloseAlertViews, PriceDropAlertViews, StationAlertHistoryListView
urlpatterns = [
    path('list/', StationAlertHistoryListView.as_view(), name='alert-list'),
    path('open_close_alert_setting/', OpenCloseAlertViews.as_view(), name='open-close-alert-setting'),
    path('price_drop_alert_setting/', PriceDropAlertViews.as_view(), name='price-drop-alert-setting'),
]
