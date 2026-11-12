"""Alerts app views."""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from .models import Alert, NotificationLog
from .forms import AlertForm


@login_required
def alert_list(request):
    alerts = Alert.objects.select_related('forest_area', 'sensor_node').order_by('-created_at')
    severity_filter = request.GET.get('severity')
    status_filter = request.GET.get('status')
    if severity_filter:
        alerts = alerts.filter(severity=severity_filter)
    if status_filter:
        alerts = alerts.filter(status=status_filter)
    paginator = Paginator(alerts, 20)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'alerts/alert_list.html',
                  {'page_obj': page_obj, 'title': 'Alert Management',
                   'severity_filter': severity_filter, 'status_filter': status_filter})


@login_required
def alert_detail(request, pk):
    alert = get_object_or_404(Alert, pk=pk)
    logs = alert.notification_logs.all()
    return render(request, 'alerts/alert_detail.html',
                  {'alert': alert, 'logs': logs, 'title': f'Alert: {alert.alert_id}'})


@login_required
def alert_create(request):
    if not request.user.is_admin:
        messages.error(request, 'Only administrators can create manual alerts.')
        return redirect('alerts:alert_list')
    form = AlertForm(request.POST or None)
    if form.is_valid():
        alert = form.save()
        send_alert_notification(alert, request.user.email)
        messages.success(request, f'Alert {alert.alert_id} created.')
        return redirect('alerts:alert_detail', pk=alert.pk)
    return render(request, 'alerts/alert_form.html',
                  {'form': form, 'title': 'Create Alert', 'action': 'Create'})


@login_required
def alert_acknowledge(request, pk):
    alert = get_object_or_404(Alert, pk=pk)
    if request.method == 'POST':
        if alert.status == 'active':
            alert.status = 'acknowledged'
            alert.acknowledged_at = timezone.now()
            alert.acknowledged_by = request.user
            alert.save()
            messages.success(request, f'Alert {alert.alert_id} acknowledged.')
        else:
            messages.warning(request, 'Alert is not in active state.')
    return redirect('alerts:alert_detail', pk=pk)


@login_required
def alert_resolve(request, pk):
    alert = get_object_or_404(Alert, pk=pk)
    if request.method == 'POST':
        alert.status = request.POST.get('status', 'resolved')
        alert.resolved_at = timezone.now()
        alert.save()
        messages.success(request, f'Alert {alert.alert_id} marked as {alert.status}.')
    return redirect('alerts:alert_detail', pk=pk)


def send_alert_notification(alert, recipient_email=None):
    """Send email notification for an alert (safe mock if not configured)."""
    log_status = 'demo'
    error_msg = ''

    if recipient_email and settings.EMAIL_HOST_USER:
        try:
            send_mail(
                subject=f'[{alert.severity.upper()}] Forest Fire Alert: {alert.title}',
                message=f'{alert.message}\n\nAlert ID: {alert.alert_id}\nTime: {alert.created_at}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient_email],
                fail_silently=True,
            )
            log_status = 'sent'
            alert.email_sent = True
            alert.save(update_fields=['email_sent'])
        except Exception as e:
            log_status = 'failed'
            error_msg = str(e)
    else:
        # Demo/console mode
        print(f"\n[ALERT NOTIFICATION - DEMO MODE]\n"
              f"Alert ID: {alert.alert_id}\n"
              f"Severity: {alert.severity.upper()}\n"
              f"Title: {alert.title}\n"
              f"Message: {alert.message}\n"
              f"Time: {alert.created_at}\n")

    NotificationLog.objects.create(
        alert=alert,
        channel='email',
        recipient=recipient_email or 'console',
        status=log_status,
        error_message=error_msg,
    )

    # SMS mock
    if settings.TWILIO_ACCOUNT_SID:
        NotificationLog.objects.create(
            alert=alert,
            channel='sms',
            recipient='configured_number',
            status='demo',
            response_data={'note': 'SMS integration point — configure Twilio credentials'},
        )
