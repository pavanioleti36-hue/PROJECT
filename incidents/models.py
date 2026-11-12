"""
Incidents app models.
Covers Modules 10 (Fire Incident) and 12 (Historical Data).
"""

from django.db import models
from django.conf import settings
from django.utils import timezone
from forest_env.models import Forest, ForestArea


class FireIncident(models.Model):
    """A confirmed or suspected fire incident."""
    SEVERITY_CHOICES = [
        ('minor', 'Minor'),
        ('moderate', 'Moderate'),
        ('major', 'Major'),
        ('catastrophic', 'Catastrophic'),
    ]
    STATUS_CHOICES = [
        ('suspected', 'Suspected'),
        ('confirmed', 'Confirmed'),
        ('under_control', 'Under Control'),
        ('extinguished', 'Extinguished'),
        ('false_alarm', 'False Alarm'),
    ]

    incident_id = models.CharField(max_length=50, unique=True, blank=True)
    forest = models.ForeignKey(Forest, on_delete=models.SET_NULL, null=True,
                                related_name='fire_incidents')
    forest_area = models.ForeignKey(ForestArea, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='fire_incidents')
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)

    # Location
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    location_description = models.CharField(max_length=500, blank=True)

    severity = models.CharField(max_length=15, choices=SEVERITY_CHOICES, default='minor')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='suspected')

    fire_start_time = models.DateTimeField(default=timezone.now)
    fire_end_time = models.DateTimeField(null=True, blank=True)
    area_burned_hectares = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    estimated_damage = models.TextField(blank=True)

    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='reported_incidents'
    )
    reported_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_simulated = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.incident_id:
            import uuid
            self.incident_id = f"INC-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.incident_id}: {self.title}"

    @property
    def duration_hours(self):
        if self.fire_end_time and self.fire_start_time:
            delta = self.fire_end_time - self.fire_start_time
            return round(delta.total_seconds() / 3600, 1)
        return None

    class Meta:
        ordering = ['-fire_start_time']
        verbose_name = 'Fire Incident'


class IncidentUpdate(models.Model):
    """Progress/status updates for a fire incident."""
    incident = models.ForeignKey(FireIncident, on_delete=models.CASCADE, related_name='updates')
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        related_name='incident_updates'
    )
    update_text = models.TextField()
    new_status = models.CharField(max_length=20, choices=FireIncident.STATUS_CHOICES, blank=True)
    new_severity = models.CharField(max_length=15, choices=FireIncident.SEVERITY_CHOICES, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Update for {self.incident.incident_id} at {self.updated_at:%Y-%m-%d %H:%M}"

    class Meta:
        ordering = ['-updated_at']
