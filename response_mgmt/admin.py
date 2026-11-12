from django.contrib import admin
from .models import (EmergencyResponse, FireSuppression, EvacuationManagement,
                     RescueOperation, ResourceAllocation)


@admin.register(EmergencyResponse)
class EmergencyResponseAdmin(admin.ModelAdmin):
    list_display = ['incident', 'response_team', 'status', 'dispatched_at', 'personnel_count']
    list_filter = ['status']


@admin.register(FireSuppression)
class FireSuppressionAdmin(admin.ModelAdmin):
    list_display = ['incident', 'method', 'effectiveness', 'started_at']
    list_filter = ['effectiveness']


@admin.register(EvacuationManagement)
class EvacuationAdmin(admin.ModelAdmin):
    list_display = ['incident', 'evacuation_zone', 'people_evacuated', 'started_at']


@admin.register(RescueOperation)
class RescueOperationAdmin(admin.ModelAdmin):
    list_display = ['incident', 'operation_name', 'people_rescued', 'status']
    list_filter = ['status']


@admin.register(ResourceAllocation)
class ResourceAllocationAdmin(admin.ModelAdmin):
    list_display = ['incident', 'resource_type', 'resource_name', 'quantity', 'status']
    list_filter = ['resource_type', 'status']
