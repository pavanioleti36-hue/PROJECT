from django.urls import path
from . import views

app_name = 'alerts'

urlpatterns = [
    path('', views.alert_list, name='alert_list'),
    path('<int:pk>/', views.alert_detail, name='alert_detail'),
    path('create/', views.alert_create, name='alert_create'),
    path('<int:pk>/acknowledge/', views.alert_acknowledge, name='alert_acknowledge'),
    path('<int:pk>/resolve/', views.alert_resolve, name='alert_resolve'),
]
