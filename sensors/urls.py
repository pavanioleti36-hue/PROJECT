from django.urls import path
from . import views

app_name = 'sensors'

urlpatterns = [
    path('', views.node_list, name='node_list'),
    path('<int:pk>/', views.node_detail, name='node_detail'),
    path('add/', views.node_create, name='node_create'),
    path('<int:pk>/edit/', views.node_update, name='node_update'),
    path('<int:pk>/delete/', views.node_delete, name='node_delete'),
    path('<int:pk>/simulate/', views.simulate_reading, name='simulate_reading'),
    path('readings/', views.reading_list, name='reading_list'),
    path('readings/add/', views.reading_create, name='reading_create'),
]
