"""
Response Management app models.
Covers Module 11 (Response and Management).
"""

from django.db import models
from django.conf import settings
from django.utils import timezone
from incidents.models import FireIncident
from forest_env.models import ForestArea


class EmergencyResponse(models.Model):
    """Records emergency response operations for a fire incident."""
    RESPONSE_STATUS = [
        ('dispatched', 'Dispatched'),
        ('on_site', 'On Site'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    incident = models.ForeignKey(FireIncident, on_delete=models.CASCADE, related_name='responses')
    response_team = models.CharField(max_length=200)
    response_leader = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='led_responses'
    )
    status = models.CharField(max_length=20, choices=RESPONSE_STATUS, default='dispatched')
    dispatched_at = models.DateTimeField(default=timezone.now)
    arrived_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    personnel_count = models.PositiveIntegerField(default=0)
    vehicles = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Response for {self.incident.incident_id} — {self.response_team}"

    class Meta:
        ordering = ['-dispatched_at']


class FireSuppression(models.Model):
    """Fire suppression operations."""
    incident = models.ForeignKey(FireIncident, on_delete=models.CASCADE,
                                  related_name='suppression_ops')
    method = models.CharField(max_length=200, help_text='e.g., Water tanker, Aerial, Fire break')
    resources_used = models.TextField(blank=True)
    water_used_liters = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    effectiveness = models.CharField(max_length=20, choices=[
        ('low', 'Low'), ('medium', 'Medium'), ('high', 'High')
    ], default='medium')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Suppression ({self.method}) for {self.incident.incident_id}"

    class Meta:
        ordering = ['-started_at']


class EvacuationManagement(models.Model):
    """Evacuation management for fire incidents."""
    incident = models.ForeignKey(FireIncident, on_delete=models.CASCADE, related_name='evacuations')
    evacuation_zone = models.CharField(max_length=200)
    people_evacuated = models.PositiveIntegerField(default=0)
    evacuation_route = models.TextField(blank=True)
    shelter_location = models.CharField(max_length=300, blank=True)
    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    coordinator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='coordinated_evacuations'
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Evacuation of {self.evacuation_zone} for {self.incident.incident_id}"

    class Meta:
        ordering = ['-started_at']


class RescueOperation(models.Model):
    """Rescue operations during fire incidents."""
    incident = models.ForeignKey(FireIncident, on_delete=models.CASCADE, related_name='rescues')
    operation_name = models.CharField(max_length=200)
    people_rescued = models.PositiveIntegerField(default=0)
    people_missing = models.PositiveIntegerField(default=0)
    rescue_team = models.CharField(max_length=200)
    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('ongoing', 'Ongoing'), ('completed', 'Completed'), ('suspended', 'Suspended')
    ], default='ongoing')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Rescue: {self.operation_name} for {self.incident.incident_id}"


class ResourceAllocation(models.Model):
    """Tracks resource allocation for incident management."""
    RESOURCE_TYPES = [
        ('personnel', 'Personnel'),
        ('vehicle', 'Vehicle'),
        ('equipment', 'Equipment'),
        ('medical', 'Medical Supply'),
        ('water', 'Water Supply'),
        ('other', 'Other'),
    ]

    incident = models.ForeignKey(FireIncident, on_delete=models.CASCADE, related_name='resources')
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    resource_name = models.CharField(max_length=200)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    unit = models.CharField(max_length=50, blank=True, help_text='e.g., persons, vehicles, liters')
    allocated_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=[
        ('allocated', 'Allocated'), ('in_use', 'In Use'), ('returned', 'Returned')
    ], default='allocated')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.resource_name} ({self.quantity} {self.unit}) for {self.incident.incident_id}"

    class Meta:
        ordering = ['-allocated_at']
