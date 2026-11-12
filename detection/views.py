"""Detection app views — risk assessment, thresholds, detection status."""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import FireRiskAssessment, ThresholdConfig
from .forms import ThresholdForm
from forest_env.models import ForestArea
from sensors.models import SensorNode, SensorData


@login_required
def risk_dashboard(request):
    assessments = FireRiskAssessment.objects.select_related('forest_area__forest').order_by('-assessed_at')[:50]
    # Latest per area
    areas = ForestArea.objects.all()
    area_risks = []
    for area in areas:
        latest = FireRiskAssessment.objects.filter(forest_area=area).order_by('-assessed_at').first()
        area_risks.append({'area': area, 'assessment': latest})
    return render(request, 'detection/risk_dashboard.html',
                  {'assessments': assessments, 'area_risks': area_risks, 'title': 'Fire Risk Assessment'})


@login_required
def risk_detail(request, pk):
    assessment = get_object_or_404(FireRiskAssessment, pk=pk)
    return render(request, 'detection/risk_detail.html',
                  {'assessment': assessment, 'title': 'Risk Assessment Detail'})


@login_required
def detection_status(request):
    """Shows current detection state across all active nodes."""
    nodes = SensorNode.objects.filter(status='active').select_related('forest_area__forest')
    node_status = []
    for node in nodes:
        latest = node.sensor_readings.order_by('-timestamp').first()
        node_status.append({'node': node, 'reading': latest})

    # Count by condition
    conditions = {'normal': 0, 'warning': 0, 'fire_suspected': 0, 'fire_detected': 0}
    for item in node_status:
        if item['reading']:
            cond = item['reading'].condition
            if cond in conditions:
                conditions[cond] += 1
        else:
            conditions['normal'] += 1

    return render(request, 'detection/detection_status.html',
                  {'node_status': node_status, 'conditions': conditions, 'title': 'Detection Status'})


@login_required
def threshold_list(request):
    thresholds = ThresholdConfig.objects.all()
    return render(request, 'detection/threshold_list.html',
                  {'thresholds': thresholds, 'title': 'Threshold Configurations'})


@login_required
def threshold_create(request):
    form = ThresholdForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Threshold configuration created.')
        return redirect('detection:threshold_list')
    return render(request, 'detection/threshold_form.html',
                  {'form': form, 'title': 'Add Threshold Config', 'action': 'Create'})


@login_required
def threshold_update(request, pk):
    obj = get_object_or_404(ThresholdConfig, pk=pk)
    form = ThresholdForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Threshold configuration updated.')
        return redirect('detection:threshold_list')
    return render(request, 'detection/threshold_form.html',
                  {'form': form, 'title': 'Edit Threshold Config', 'action': 'Update', 'object': obj})


@login_required
def run_assessment(request, area_id):
    """Run a fresh fire risk assessment for a forest area."""
    area = get_object_or_404(ForestArea, pk=area_id)
    if request.method == 'POST':
        # Get latest reading per node in this area
        nodes = SensorNode.objects.filter(forest_area=area, status='active')
        readings = []
        for node in nodes:
            latest = node.sensor_readings.order_by('-timestamp').first()
            if latest:
                readings.append(latest)

        if not readings:
            messages.warning(request, 'No active sensor data found for this area.')
            return redirect('detection:risk_dashboard')

        # Average risk scores
        avg_temp_risk = sum(r.temperature_risk for r in readings) / len(readings)
        avg_smoke_risk = sum(r.smoke_risk for r in readings) / len(readings)
        avg_flame_risk = sum(r.flame_risk for r in readings) / len(readings)
        avg_humidity_risk = sum(r.humidity_risk for r in readings) / len(readings)
        avg_overall = sum(float(r.fire_risk_score or 0) for r in readings) / len(readings)

        # Get worst condition
        condition_order = ['normal', 'warning', 'fire_suspected', 'fire_detected']
        worst = max(readings, key=lambda r: condition_order.index(r.condition))

        assessment = FireRiskAssessment.objects.create(
            forest_area=area,
            temperature_risk=round(avg_temp_risk, 2),
            smoke_risk=round(avg_smoke_risk, 2),
            flame_risk=round(avg_flame_risk, 2),
            humidity_risk=round(avg_humidity_risk, 2),
            overall_risk_score=round(avg_overall, 2),
            risk_level=worst.risk_level,
            condition=worst.condition,
            active_nodes=len(nodes),
            readings_count=len(readings),
        )
        messages.success(request, f'Assessment complete. Overall risk: {assessment.risk_level.upper()}')
        return redirect('detection:risk_detail', pk=assessment.pk)

    return redirect('detection:risk_dashboard')
