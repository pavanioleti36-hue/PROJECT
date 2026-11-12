from django.contrib import admin
from .models import FireIncident, IncidentUpdate


class IncidentUpdateInline(admin.TabularInline):
    model = IncidentUpdate
    extra = 0
    readonly_fields = ['updated_at']


@admin.register(FireIncident)
class FireIncidentAdmin(admin.ModelAdmin):
    list_display = ['incident_id', 'title', 'forest', 'severity', 'status',
                    'fire_start_time', 'is_simulated']
    list_filter = ['severity', 'status', 'is_simulated']
    search_fields = ['incident_id', 'title', 'description']
    readonly_fields = ['incident_id', 'reported_at', 'updated_at']
    inlines = [IncidentUpdateInline]
    date_hierarchy = 'fire_start_time'


@admin.register(IncidentUpdate)
class IncidentUpdateAdmin(admin.ModelAdmin):
    list_display = ['incident', 'new_status', 'updated_by', 'updated_at']
    list_filter = ['new_status']
