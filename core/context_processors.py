"""Global context processors for the Forest Fire Detection System."""

from alerts.models import Alert


def alert_context(request):
    """Inject active_alert_count into every template context."""
    if request.user.is_authenticated:
        try:
            count = Alert.objects.filter(status='active').count()
        except Exception:
            count = 0
        return {'active_alert_count': count}
    return {'active_alert_count': 0}
