from django.contrib import admin
from .models import FireRiskAssessment, DataValidationLog, ThresholdConfig


@admin.register(FireRiskAssessment)
class FireRiskAssessmentAdmin(admin.ModelAdmin):
    list_display = ['forest_area', 'overall_risk_score', 'risk_level', 'condition', 'assessed_at']
    list_filter = ['risk_level', 'condition']
    date_hierarchy = 'assessed_at'


@admin.register(DataValidationLog)
class DataValidationLogAdmin(admin.ModelAdmin):
    list_display = ['sensor_data', 'is_valid', 'filtered_out', 'validated_at']
    list_filter = ['is_valid', 'filtered_out']


@admin.register(ThresholdConfig)
class ThresholdConfigAdmin(admin.ModelAdmin):
    list_display = ['name', 'temp_warning', 'temp_fire_suspected', 'smoke_warning',
                    'is_active', 'updated_at']
    list_filter = ['is_active']
