from django.contrib import admin
from .models import Alert, NotificationLog


class NotificationLogInline(admin.TabularInline):
    model = NotificationLog
    extra = 0
    readonly_fields = ['sent_at']


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['alert_id', 'severity', 'status', 'forest_area', 'title', 'created_at',
                    'email_sent', 'sms_sent']
    list_filter = ['severity', 'status', 'email_sent', 'sms_sent', 'is_simulated']
    search_fields = ['alert_id', 'title', 'message']
    readonly_fields = ['alert_id', 'created_at', 'acknowledged_at', 'resolved_at']
    inlines = [NotificationLogInline]
    date_hierarchy = 'created_at'


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ['alert', 'channel', 'recipient', 'status', 'sent_at']
    list_filter = ['channel', 'status']
