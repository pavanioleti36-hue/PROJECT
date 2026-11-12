"""
Detection app models.
Covers Modules 4 (Data Processing), 5 (Fire Detection), and 6 (Fire Risk Assessment).
"""

from django.db import models
from django.utils import timezone
from sensors.models import SensorData, SensorNode
from forest_env.models import ForestArea


class FireRiskAssessment(models.Model):
    """Aggregated risk assessment for a forest area at a given time."""
    RISK_LEVEL_CHOICES = [
        ('low', 'LOW'),
        ('medium', 'MEDIUM'),
        ('high', 'HIGH'),
        ('critical', 'CRITICAL'),
    ]
    CONDITION_CHOICES = [
        ('normal', 'Normal Condition'),
        ('warning', 'Warning Condition'),
        ('fire_suspected', 'Fire Suspected'),
        ('fire_detected', 'Fire Detected'),
    ]

    forest_area = models.ForeignKey(ForestArea, on_delete=models.CASCADE,
                                     related_name='risk_assessments')
    assessed_at = models.DateTimeField(default=timezone.now)

    # Individual risk scores (0-100)
    temperature_risk = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    smoke_risk = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    flame_risk = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    humidity_risk = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    weather_risk = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    overall_risk_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    risk_level = models.CharField(max_length=10, choices=RISK_LEVEL_CHOICES, default='low')
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='normal')

    active_nodes = models.PositiveIntegerField(default=0)
    readings_count = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Risk [{self.risk_level.upper()}] @ {self.forest_area} — {self.assessed_at:%Y-%m-%d %H:%M}"

    class Meta:
        ordering = ['-assessed_at']
        verbose_name = 'Fire Risk Assessment'


class DataValidationLog(models.Model):
    """Records data validation and filtering results."""
    sensor_data = models.ForeignKey(SensorData, on_delete=models.CASCADE,
                                     related_name='validation_logs')
    validated_at = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)
    validation_errors = models.JSONField(default=dict)
    filtered_out = models.BooleanField(default=False)
    filter_reason = models.CharField(max_length=200, blank=True)

    def __str__(self):
        status = 'VALID' if self.is_valid else 'INVALID'
        return f"{status}: {self.sensor_data}"

    class Meta:
        ordering = ['-validated_at']


class ThresholdConfig(models.Model):
    """Configurable threshold settings for fire detection."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    # Temperature thresholds
    temp_warning = models.DecimalField(max_digits=5, decimal_places=2, default=45.0)
    temp_fire_suspected = models.DecimalField(max_digits=5, decimal_places=2, default=60.0)
    temp_fire_detected = models.DecimalField(max_digits=5, decimal_places=2, default=80.0)

    # Smoke thresholds (ppm)
    smoke_warning = models.DecimalField(max_digits=7, decimal_places=2, default=150.0)
    smoke_fire_suspected = models.DecimalField(max_digits=7, decimal_places=2, default=300.0)
    smoke_fire_detected = models.DecimalField(max_digits=7, decimal_places=2, default=500.0)

    # Humidity thresholds (%)
    humidity_warning = models.DecimalField(max_digits=5, decimal_places=2, default=35.0)
    humidity_critical = models.DecimalField(max_digits=5, decimal_places=2, default=20.0)

    # Gas concentration thresholds (ppm)
    gas_warning = models.DecimalField(max_digits=7, decimal_places=2, default=100.0)
    gas_fire_suspected = models.DecimalField(max_digits=7, decimal_places=2, default=200.0)

    # Composite risk score thresholds (0-100)
    score_warning = models.DecimalField(max_digits=5, decimal_places=2, default=25.0)
    score_fire_suspected = models.DecimalField(max_digits=5, decimal_places=2, default=45.0)
    score_fire_detected = models.DecimalField(max_digits=5, decimal_places=2, default=70.0)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Threshold Config: {self.name}"

    class Meta:
        verbose_name = 'Threshold Configuration'
