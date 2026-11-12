from django.urls import path
from . import views

app_name = 'forest_env'

urlpatterns = [
    # Forest
    path('', views.forest_list, name='forest_list'),
    path('<int:pk>/', views.forest_detail, name='forest_detail'),
    path('add/', views.forest_create, name='forest_create'),
    path('<int:pk>/edit/', views.forest_update, name='forest_update'),
    path('<int:pk>/delete/', views.forest_delete, name='forest_delete'),
    # Forest Areas
    path('areas/', views.area_list, name='area_list'),
    path('areas/<int:pk>/', views.area_detail, name='area_detail'),
    path('areas/add/', views.area_create, name='area_create'),
    path('areas/<int:pk>/edit/', views.area_update, name='area_update'),
    path('areas/<int:pk>/delete/', views.area_delete, name='area_delete'),
    # Vegetation
    path('vegetation/', views.vegetation_list, name='vegetation_list'),
    path('vegetation/add/', views.vegetation_create, name='vegetation_create'),
    path('vegetation/<int:pk>/edit/', views.vegetation_update, name='vegetation_update'),
    path('vegetation/<int:pk>/delete/', views.vegetation_delete, name='vegetation_delete'),
    # Wildlife
    path('wildlife/', views.wildlife_list, name='wildlife_list'),
    path('wildlife/add/', views.wildlife_create, name='wildlife_create'),
    path('wildlife/<int:pk>/edit/', views.wildlife_update, name='wildlife_update'),
    path('wildlife/<int:pk>/delete/', views.wildlife_delete, name='wildlife_delete'),
    # Weather
    path('weather/', views.weather_list, name='weather_list'),
    path('weather/add/', views.weather_create, name='weather_create'),
    path('weather/<int:pk>/edit/', views.weather_update, name='weather_update'),
    path('weather/<int:pk>/delete/', views.weather_delete, name='weather_delete'),
]
