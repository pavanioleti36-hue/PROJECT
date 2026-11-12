"""
Sensors app models.
Covers Modules 2 (Sensor), 3 (Data Collection), and 8 (Location & Monitoring).
"""

from django.db import models
from django.utils import timezone
from forest_env.models import ForestArea


class SensorNode(models.Model):
    """Physical sensor node deployed in the field."""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Under Maintenance'),
        ('faulty', 'Faulty'),
    ]
    node_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    forest_area = models.ForeignKey(ForestArea, on_delete=models.SET_NULL, null=True,
                                    related_name='sensor_nodes')
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    altitude_m = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    installed_at = models.DateTimeField(default=timezone.now)
    last_seen = models.DateTimeField(null=True, blank=True)
    battery_level = models.PositiveSmallIntegerField(null=True, blank=True, help_text='0-100 %')
    notes = models.TextField(blank=True)
    is_simulated = models.BooleanField(default=False,
                                        help_text='True if this is a simulated/demo node')

    def __str__(self):
        return f"{self.node_id} — {self.name}"

    @property
    def is_active(self):
        return self.status == 'active'

    class Meta:
        ordering = ['node_id']


class TemperatureSensor(models.Model):
    node = models.OneToOneField(SensorNode, on_delete=models.CASCADE, related_name='temp_sensor')
    model_number = models.CharField(max_length=100, blank=True)
    min_range = models.DecimalField(max_digits=6, decimal_places=2, default=-40)
    max_range = models.DecimalField(max_digits=6, decimal_places=2, default=125)
    fire_threshold = models.DecimalField(max_digits=5, decimal_places=2, default=60.0,
                                          help_text='°C above which fire is suspected')
    warning_threshold = models.DecimalField(max_digits=5, decimal_places=2, default=45.0)
    calibrated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Temp Sensor @ {self.node}"


class SmokeSensor(models.Model):
    node = models.OneToOneField(SensorNode, on_delete=models.CASCADE, related_name='smoke_sensor')
    model_number = models.CharField(max_length=100, blank=True)
    fire_threshold = models.DecimalField(max_digits=6, decimal_places=2, default=300.0,
                                          help_text='ppm above which fire is suspected')
    warning_threshold = models.DecimalField(max_digits=6, decimal_places=2, default=150.0)
    calibrated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Smoke Sensor @ {self.node}"


class FlameSensor(models.Model):
    node = models.OneToOneField(SensorNode, on_delete=models.CASCADE, related_name='flame_sensor')
    model_number = models.CharField(max_length=100, blank=True)
    detection_angle = models.PositiveSmallIntegerField(default=60, help_text='degrees')
    calibrated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Flame Sensor @ {self.node}"


class HumiditySensor(models.Model):
    node = models.OneToOneField(SensorNode, on_delete=models.CASCADE, related_name='humidity_sensor')
    model_number = models.CharField(max_length=100, blank=True)
    low_threshold = models.DecimalField(max_digits=5, decimal_places=2, default=20.0,
                                         help_text='% RH below which fire risk is HIGH')
    warning_threshold = models.DecimalField(max_digits=5, decimal_places=2, default=35.0)
    calibrated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Humidity Sensor @ {self.node}"


class GasSensor(models.Model):
    node = models.OneToOneField(SensorNode, on_delete=models.CASCADE, related_name='gas_sensor')
    model_number = models.CharField(max_length=100, blank=True)
    gas_type = models.CharField(max_length=50, default='CO', help_text='e.g., CO, CO2, LPG')
    fire_threshold = models.DecimalField(max_digits=6, decimal_places=2, default=200.0,
                                          help_text='ppm above which fire is suspected')
    warning_threshold = models.DecimalField(max_digits=6, decimal_places=2, default=100.0)
    calibrated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Gas Sensor ({self.gas_type}) @ {self.node}"


class SensorData(models.Model):
    """Unified sensor reading record (one reading per timestamp per node)."""
    CONDITION_CHOICES = [
        ('normal', 'Normal Condition'),
        ('warning', 'Warning Condition'),
        ('fire_suspected', 'Fire Suspected'),
        ('fire_detected', 'Fire Detected'),
    ]
    RISK_LEVEL_CHOICES = [
        ('low', 'LOW'),
        ('medium', 'MEDIUM'),
        ('high', 'HIGH'),
        ('critical', 'CRITICAL'),
    ]

    node = models.ForeignKey(SensorNode, on_delete=models.CASCADE, related_name='sensor_readings')
    timestamp = models.DateTimeField(default=timezone.now)

    # Raw sensor values
    temperature = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True,
                                       help_text='°C')
    humidity = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                    help_text='%')
    smoke_level = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True,
                                       help_text='ppm')
    gas_concentration = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True,
                                             help_text='ppm')
    flame_detected = models.BooleanField(default=False)
    flame_intensity = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                           help_text='0-100 scale')

    # Computed fields
    fire_risk_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                           help_text='0-100 composite risk score')
    risk_level = models.CharField(max_length=10, choices=RISK_LEVEL_CHOICES, default='low')
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='normal')

    is_simulated = models.BooleanField(default=False)
    is_valid = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.node.node_id} @ {self.timestamp:%Y-%m-%d %H:%M} [{self.condition}]"

    @property
    def temperature_risk(self):
        """Returns 0-100 risk score for temperature."""
        if self.temperature is None:
            return 0
        t = float(self.temperature)
        if t >= 80:
            return 100
        elif t >= 60:
            return 80
        elif t >= 45:
            return 50
        elif t >= 35:
            return 25
        return 10

    @property
    def smoke_risk(self):
        if self.smoke_level is None:
            return 0
        s = float(self.smoke_level)
        if s >= 500:
            return 100
        elif s >= 300:
            return 80
        elif s >= 150:
            return 50
        elif s >= 80:
            return 25
        return 5

    @property
    def humidity_risk(self):
        if self.humidity is None:
            return 50
        h = float(self.humidity)
        if h <= 15:
            return 100
        elif h <= 25:
            return 80
        elif h <= 35:
            return 50
        elif h <= 50:
            return 25
        return 5

    @property
    def gas_risk(self):
        if self.gas_concentration is None:
            return 0
        g = float(self.gas_concentration)
        if g >= 400:
            return 100
        elif g >= 200:
            return 80
        elif g >= 100:
            return 50
        elif g >= 50:
            return 25
        return 5

    @property
    def flame_risk(self):
        if self.flame_detected:
            intensity = float(self.flame_intensity or 50)
            return min(100, 70 + intensity * 0.3)
        return 0

    def calculate_risk(self):
        """Compute composite fire risk score and update fields."""
        weights = {
            'temperature': 0.30,
            'smoke': 0.25,
            'flame': 0.25,
            'humidity': 0.10,
            'gas': 0.10,
        }
        score = (
            self.temperature_risk * weights['temperature'] +
            self.smoke_risk * weights['smoke'] +
            self.flame_risk * weights['flame'] +
            self.humidity_risk * weights['humidity'] +
            self.gas_risk * weights['gas']
        )
        self.fire_risk_score = round(score, 2)

        if self.flame_detected and score >= 70:
            self.condition = 'fire_detected'
            self.risk_level = 'critical'
        elif score >= 70 or (self.flame_detected and score >= 50):
            self.condition = 'fire_suspected'
            self.risk_level = 'critical'
        elif score >= 45:
            self.condition = 'warning'
            self.risk_level = 'high'
        elif score >= 25:
            self.condition = 'warning'
            self.risk_level = 'medium'
        else:
            self.condition = 'normal'
            self.risk_level = 'low'

    def save(self, *args, **kwargs):
        self.calculate_risk()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Sensor Reading'
        verbose_name_plural = 'Sensor Readings'
