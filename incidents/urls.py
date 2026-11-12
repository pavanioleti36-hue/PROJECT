from django.urls import path
from . import views

app_name = 'incidents'

urlpatterns = [
    path('', views.incident_list, name='incident_list'),
    path('<int:pk>/', views.incident_detail, name='incident_detail'),
    path('report/', views.incident_create, name='incident_create'),
    path('<int:pk>/edit/', views.incident_update, name='incident_update'),
    path('<int:pk>/delete/', views.incident_delete, name='incident_delete'),
    path('<int:pk>/update/', views.incident_add_update, name='incident_add_update'),
    path('export/csv/', views.export_incidents_csv, name='export_csv'),
]
