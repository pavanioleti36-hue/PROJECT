from django.contrib import admin
from .models import (Forest, ForestArea, Vegetation, Wildlife, WeatherCondition)


@admin.register(Forest)
class ForestAdmin(admin.ModelAdmin):
    list_display = ['name', 'state', 'district', 'is_protected', 'total_area_hectares']
    list_filter = ['state', 'is_protected']
    search_fields = ['name', 'state', 'district']


@admin.register(ForestArea)
class ForestAreaAdmin(admin.ModelAdmin):
    list_display = ['name', 'forest', 'zone_type', 'area_hectares', 'is_high_risk']
    list_filter = ['zone_type', 'is_high_risk', 'forest']
    search_fields = ['name', 'forest__name']


@admin.register(Vegetation)
class VegetationAdmin(admin.ModelAdmin):
    list_display = ['vegetation_type', 'forest_area', 'density', 'fire_susceptibility']
    list_filter = ['density', 'fire_susceptibility']


@admin.register(Wildlife)
class WildlifeAdmin(admin.ModelAdmin):
    list_display = ['species_name', 'forest_area', 'conservation_status']
    list_filter = ['conservation_status']


@admin.register(WeatherCondition)
class WeatherConditionAdmin(admin.ModelAdmin):
    list_display = ['forest_area', 'temperature', 'humidity', 'wind_speed', 'recorded_at']
    list_filter = ['forest_area']
