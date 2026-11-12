from django.urls import path
from . import views

app_name = 'detection'

urlpatterns = [
    path('', views.risk_dashboard, name='risk_dashboard'),
    path('status/', views.detection_status, name='status'),
    path('assessment/<int:pk>/', views.risk_detail, name='risk_detail'),
    path('assessment/run/<int:area_id>/', views.run_assessment, name='run_assessment'),
    path('thresholds/', views.threshold_list, name='threshold_list'),
    path('thresholds/add/', views.threshold_create, name='threshold_create'),
    path('thresholds/<int:pk>/edit/', views.threshold_update, name='threshold_update'),
]
