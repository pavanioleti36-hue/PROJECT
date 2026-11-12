"""
Forest Environment app models.
Covers Modules 1 (Forest Environment) and 8 (Location & Monitoring).
"""

from django.db import models
from django.utils import timezone


class Forest(models.Model):
    """Represents a named forest area."""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    established_year = models.PositiveIntegerField(null=True, blank=True)
    total_area_hectares = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    forest_type = models.CharField(max_length=100, blank=True,
                                   help_text='e.g., Tropical, Deciduous, Evergreen')
    is_protected = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class ForestArea(models.Model):
    """A zone/section within a forest."""
    ZONE_TYPES = [
        ('core', 'Core Zone'),
        ('buffer', 'Buffer Zone'),
        ('transition', 'Transition Zone'),
        ('peripheral', 'Peripheral Zone'),
    ]
    forest = models.ForeignKey(Forest, on_delete=models.CASCADE, related_name='areas')
    name = models.CharField(max_length=200)
    zone_type = models.CharField(max_length=20, choices=ZONE_TYPES, default='core')
    area_hectares = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    description = models.TextField(blank=True)
    is_high_risk = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.forest.name} — {self.name}"

    class Meta:
        ordering = ['forest', 'name']


class Vegetation(models.Model):
    """Vegetation data for a forest area."""
    DENSITY_CHOICES = [
        ('sparse', 'Sparse'),
        ('moderate', 'Moderate'),
        ('dense', 'Dense'),
        ('very_dense', 'Very Dense'),
    ]
    forest_area = models.ForeignKey(ForestArea, on_delete=models.CASCADE, related_name='vegetations')
    vegetation_type = models.CharField(max_length=200)
    density = models.CharField(max_length=20, choices=DENSITY_CHOICES, default='moderate')
    moisture_content = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                           help_text='Percentage moisture content')
    fire_susceptibility = models.CharField(max_length=20, choices=[
        ('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('critical', 'Critical')
    ], default='medium')
    notes = models.TextField(blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vegetation_type} @ {self.forest_area}"

    class Meta:
        ordering = ['-recorded_at']


class Wildlife(models.Model):
    """Wildlife species found in a forest area."""
    STATUS_CHOICES = [
        ('abundant', 'Abundant'),
        ('common', 'Common'),
        ('rare', 'Rare'),
        ('endangered', 'Endangered'),
    ]
    forest_area = models.ForeignKey(ForestArea, on_delete=models.CASCADE, related_name='wildlife')
    species_name = models.CharField(max_length=200)
    scientific_name = models.CharField(max_length=200, blank=True)
    population_estimate = models.PositiveIntegerField(null=True, blank=True)
    conservation_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='common')
    notes = models.TextField(blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.species_name} @ {self.forest_area}"

    class Meta:
        verbose_name_plural = 'Wildlife'
        ordering = ['species_name']


class WeatherCondition(models.Model):
    """Current / recent weather data for a forest area."""
    forest_area = models.ForeignKey(ForestArea, on_delete=models.CASCADE, related_name='weather_conditions')
    temperature = models.DecimalField(max_digits=5, decimal_places=2, help_text='°C')
    humidity = models.DecimalField(max_digits=5, decimal_places=2, help_text='%')
    wind_speed = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text='km/h')
    wind_direction = models.CharField(max_length=10, blank=True)
    rainfall = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text='mm')
    condition = models.CharField(max_length=100, blank=True, help_text='e.g., Clear, Cloudy, Rain')
    recorded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Weather @ {self.forest_area} on {self.recorded_at:%Y-%m-%d %H:%M}"

    class Meta:
        ordering = ['-recorded_at']
