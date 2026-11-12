"""
Alerts app models.
Covers Module 7 (Alert and Notification).
"""

from django.db import models
from django.conf import settings
from django.utils import timezone
from sensors.models import SensorData, SensorNode
from forest_env.models import ForestArea


class Alert(models.Model):
    """Generated alert when fire-risk conditions are detected."""
    SEVERITY_CHOICES = [
        ('info', 'Information'),
        ('warning', 'Warning'),
        ('critical', 'Critical'),
        ('emergency', 'Emergency'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('acknowledged', 'Acknowledged'),
        ('resolved', 'Resolved'),
        ('false_alarm', 'False Alarm'),
    ]

    alert_id = models.CharField(max_length=50, unique=True, blank=True)
    forest_area = models.ForeignKey(ForestArea, on_delete=models.SET_NULL, null=True,
                                     related_name='alerts')
    sensor_node = models.ForeignKey(SensorNode, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='alerts')
    trigger_data = models.ForeignKey(SensorData, on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='triggered_alerts')

    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='warning')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='active')
    title = models.CharField(max_length=300)
    message = models.TextField()
    fire_risk_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    condition = models.CharField(max_length=20, blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    acknowledged_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='acknowledged_alerts'
    )

    email_sent = models.BooleanField(default=False)
    sms_sent = models.BooleanField(default=False)
    mobile_notification_sent = models.BooleanField(default=False)

    is_simulated = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.alert_id:
            import uuid
            self.alert_id = f"ALT-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.severity.upper()}] {self.title} @ {self.created_at:%Y-%m-%d %H:%M}"

    @property
    def is_active(self):
        return self.status == 'active'

    class Meta:
        ordering = ['-created_at']


class NotificationLog(models.Model):
    """Records every notification attempt (email, SMS, mobile)."""
    CHANNEL_CHOICES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('mobile', 'Mobile Push'),
        ('emergency', 'Emergency Call'),
    ]
    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('demo', 'Demo/Mock'),
    ]

    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name='notification_logs')
    channel = models.CharField(max_length=15, choices=CHANNEL_CHOICES)
    recipient = models.CharField(max_length=200, help_text='Email address, phone number, etc.')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='demo')
    response_data = models.JSONField(default=dict, blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    error_message = models.TextField(blank=True)

    def __str__(self):
        return f"{self.channel} to {self.recipient} [{self.status}]"

    class Meta:
        ordering = ['-sent_at']
