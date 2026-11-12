"""Reports / Dashboard views."""

import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count
from django.core.paginator import Paginator
from django.utils import timezone

from forest_env.models import Forest, ForestArea
from sensors.models import SensorNode, SensorData
from detection.models import FireRiskAssessment
from alerts.models import Alert
from incidents.models import FireIncident


@login_required
def dashboard_home(request):
    # Core stats
    total_forests = Forest.objects.count()
    total_areas = ForestArea.objects.count()
    total_sensors = SensorNode.objects.count()
    active_sensors = SensorNode.objects.filter(status='active').count()
    total_alerts = Alert.objects.count()
    active_alerts = Alert.objects.filter(status='active').count()
    total_incidents = FireIncident.objects.count()
    high_risk_areas = ForestArea.objects.filter(is_high_risk=True).count()

    # Recent data
    recent_alerts = Alert.objects.select_related('forest_area').order_by('-created_at')[:5]
    recent_incidents = FireIncident.objects.select_related('forest').order_by('-fire_start_time')[:5]
    recent_readings = SensorData.objects.select_related('node__forest_area').order_by('-timestamp')[:8]

    # Current risk from latest assessment
    latest_assessment = FireRiskAssessment.objects.order_by('-assessed_at').first()
    current_risk_level = latest_assessment.risk_level if latest_assessment else 'low'
    current_risk_score = float(latest_assessment.overall_risk_score) if latest_assessment else 0

    # Timeline: readings per day for last 7 days
    today = timezone.now().date()
    timeline_labels = []
    timeline_data = []
    for i in range(6, -1, -1):
        day = today - datetime.timedelta(days=i)
        count = SensorData.objects.filter(timestamp__date=day).count()
        timeline_labels.append(day.strftime('%b %d'))
        timeline_data.append(count)

    # Risk counts for pie chart
    risk_counts = {
        'low': SensorData.objects.filter(risk_level='low').count(),
        'medium': SensorData.objects.filter(risk_level='medium').count(),
        'high': SensorData.objects.filter(risk_level='high').count(),
        'critical': SensorData.objects.filter(risk_level='critical').count(),
    }

    # Active fire conditions
    fire_detected_count = SensorData.objects.filter(
        condition='fire_detected',
        timestamp__gte=timezone.now() - datetime.timedelta(hours=24)
    ).count()
    fire_suspected_count = SensorData.objects.filter(
        condition='fire_suspected',
        timestamp__gte=timezone.now() - datetime.timedelta(hours=24)
    ).count()

    context = {
        'title': 'Dashboard',
        'total_forests': total_forests,
        'total_areas': total_areas,
        'total_sensors': total_sensors,
        'active_sensors': active_sensors,
        'total_alerts': total_alerts,
        'active_alerts': active_alerts,
        'active_alert_count': active_alerts,
        'total_incidents': total_incidents,
        'high_risk_areas': high_risk_areas,
        'recent_alerts': recent_alerts,
        'recent_incidents': recent_incidents,
        'recent_readings': recent_readings,
        'current_risk_level': current_risk_level,
        'current_risk_score': current_risk_score,
        'latest_assessment': latest_assessment,
        'timeline_labels': timeline_labels,
        'timeline_data': timeline_data,
        'risk_counts': risk_counts,
        'fire_detected_count': fire_detected_count,
        'fire_suspected_count': fire_suspected_count,
    }
    return render(request, 'reports/dashboard.html', context)


@login_required
def sensor_chart_data(request):
    """JSON API: last 50 sensor readings for Chart.js."""
    readings = SensorData.objects.order_by('-timestamp')[:50]
    readings = list(reversed(readings))
    data = {
        'labels': [r.timestamp.strftime('%H:%M %d/%m') for r in readings],
        'temperature': [float(r.temperature) if r.temperature else None for r in readings],
        'humidity': [float(r.humidity) if r.humidity else None for r in readings],
        'smoke': [float(r.smoke_level) if r.smoke_level else None for r in readings],
        'risk_score': [float(r.fire_risk_score) if r.fire_risk_score else 0 for r in readings],
    }
    return JsonResponse(data)


@login_required
def alert_history(request):
    alerts = Alert.objects.select_related('forest_area', 'sensor_node').order_by('-created_at')
    severity_filter = request.GET.get('severity')
    if severity_filter:
        alerts = alerts.filter(severity=severity_filter)
    paginator = Paginator(alerts, 20)
    page_obj = paginator.get_page(request.GET.get('page'))
    # Stats
    stats = {
        'total': Alert.objects.count(),
        'active': Alert.objects.filter(status='active').count(),
        'by_severity': {
            'info': Alert.objects.filter(severity='info').count(),
            'warning': Alert.objects.filter(severity='warning').count(),
            'critical': Alert.objects.filter(severity='critical').count(),
            'emergency': Alert.objects.filter(severity='emergency').count(),
        }
    }
    return render(request, 'reports/alert_history.html',
                  {'page_obj': page_obj, 'title': 'Alert History',
                   'stats': stats, 'severity_filter': severity_filter})


@login_required
def incident_reports(request):
    incidents = FireIncident.objects.select_related('forest', 'forest_area').order_by('-fire_start_time')
    stats = {
        'total': FireIncident.objects.count(),
        'by_severity': {
            'minor': FireIncident.objects.filter(severity='minor').count(),
            'moderate': FireIncident.objects.filter(severity='moderate').count(),
            'major': FireIncident.objects.filter(severity='major').count(),
            'catastrophic': FireIncident.objects.filter(severity='catastrophic').count(),
        },
        'by_status': {
            'suspected': FireIncident.objects.filter(status='suspected').count(),
            'confirmed': FireIncident.objects.filter(status='confirmed').count(),
            'under_control': FireIncident.objects.filter(status='under_control').count(),
            'extinguished': FireIncident.objects.filter(status='extinguished').count(),
            'false_alarm': FireIncident.objects.filter(status='false_alarm').count(),
        }
    }
    paginator = Paginator(incidents, 15)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'reports/incident_reports.html',
                  {'page_obj': page_obj, 'title': 'Incident Reports', 'stats': stats})


@login_required
def statistical_reports(request):
    from django.db.models import Avg, Max, Min, Sum
    reading_stats = SensorData.objects.aggregate(
        total=Count('id'),
        avg_temp=Avg('temperature'),
        avg_humidity=Avg('humidity'),
        avg_smoke=Avg('smoke_level'),
        max_risk=Max('fire_risk_score'),
        avg_risk=Avg('fire_risk_score'),
    )
    condition_counts = {
        'normal': SensorData.objects.filter(condition='normal').count(),
        'warning': SensorData.objects.filter(condition='warning').count(),
        'fire_suspected': SensorData.objects.filter(condition='fire_suspected').count(),
        'fire_detected': SensorData.objects.filter(condition='fire_detected').count(),
    }
    alert_counts = Alert.objects.values('severity').annotate(count=Count('id'))
    node_stats = {
        'total': SensorNode.objects.count(),
        'active': SensorNode.objects.filter(status='active').count(),
        'inactive': SensorNode.objects.filter(status='inactive').count(),
        'faulty': SensorNode.objects.filter(status='faulty').count(),
        'simulated': SensorNode.objects.filter(is_simulated=True).count(),
    }
    return render(request, 'reports/statistical_reports.html',
                  {'title': 'Statistical Reports', 'reading_stats': reading_stats,
                   'condition_counts': condition_counts, 'alert_counts': alert_counts,
                   'node_stats': node_stats})


@login_required
def fire_risk_map(request):
    import json
    areas_qs = ForestArea.objects.select_related('forest').filter(
        latitude__isnull=False, longitude__isnull=False)
    areas_data = [
        {'id': a.pk, 'name': a.name, 'forest': a.forest.name,
         'zone_type': a.get_zone_type_display(),
         'lat': float(a.latitude), 'lng': float(a.longitude),
         'is_high_risk': a.is_high_risk}
        for a in areas_qs
    ]
    incidents_qs = FireIncident.objects.filter(
        latitude__isnull=False, longitude__isnull=False)
    incidents_data = [
        {'id': i.pk, 'title': i.title,
         'severity': i.get_severity_display(), 'status': i.get_status_display(),
         'lat': float(i.latitude), 'lng': float(i.longitude)}
        for i in incidents_qs
    ]
    return render(request, 'reports/fire_risk_map.html',
                  {'title': 'Fire Risk Map',
                   'areas_json': json.dumps(areas_data),
                   'incidents_json': json.dumps(incidents_data),
                   'total_areas': len(areas_data),
                   'total_incidents': len(incidents_data)})
