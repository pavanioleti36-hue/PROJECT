from django.urls import path
from . import views

app_name = 'response_mgmt'

urlpatterns = [
    path('', views.response_list, name='response_list'),
    path('add/', views.response_create, name='response_create'),
    path('<int:pk>/edit/', views.response_update, name='response_update'),
    path('<int:pk>/delete/', views.response_delete, name='response_delete'),
    path('suppression/add/', views.suppression_create, name='suppression_create'),
    path('evacuation/add/', views.evacuation_create, name='evacuation_create'),
    path('rescue/add/', views.rescue_create, name='rescue_create'),
    path('resource/add/', views.resource_create, name='resource_create'),
]
