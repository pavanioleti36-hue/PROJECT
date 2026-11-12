from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('sensor-data/', views.sensor_chart_data, name='sensor_chart_data'),
    path('alert-history/', views.alert_history, name='alert_history'),
    path('incident-reports/', views.incident_reports, name='incident_reports'),
    path('statistical-reports/', views.statistical_reports, name='statistical_reports'),
    path('fire-risk-map/', views.fire_risk_map, name='fire_risk_map'),
]
