from django.contrib import admin
from .models import (SensorNode, TemperatureSensor, SmokeSensor, FlameSensor,
                     HumiditySensor, GasSensor, SensorData)


class TemperatureSensorInline(admin.StackedInline):
    model = TemperatureSensor
    extra = 0

class SmokeSensorInline(admin.StackedInline):
    model = SmokeSensor
    extra = 0

class FlameSensorInline(admin.StackedInline):
    model = FlameSensor
    extra = 0

class HumiditySensorInline(admin.StackedInline):
    model = HumiditySensor
    extra = 0

class GasSensorInline(admin.StackedInline):
    model = GasSensor
    extra = 0


@admin.register(SensorNode)
class SensorNodeAdmin(admin.ModelAdmin):
    list_display = ['node_id', 'name', 'forest_area', 'status', 'is_simulated', 'last_seen']
    list_filter = ['status', 'is_simulated', 'forest_area__forest']
    search_fields = ['node_id', 'name']
    inlines = [TemperatureSensorInline, SmokeSensorInline, FlameSensorInline,
                HumiditySensorInline, GasSensorInline]


@admin.register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    list_display = ['node', 'timestamp', 'temperature', 'humidity', 'smoke_level',
                    'flame_detected', 'risk_level', 'condition', 'is_simulated']
    list_filter = ['risk_level', 'condition', 'is_simulated', 'flame_detected']
    search_fields = ['node__node_id', 'node__name']
    readonly_fields = ['fire_risk_score', 'risk_level', 'condition']
    date_hierarchy = 'timestamp'
