"""Sensors app views — nodes, readings, simulate."""

import random
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from .models import SensorNode, SensorData, TemperatureSensor, SmokeSensor, FlameSensor, HumiditySensor, GasSensor
from .forms import SensorNodeForm, SensorDataForm


@login_required
def node_list(request):
    nodes = SensorNode.objects.select_related('forest_area__forest').all()
    status_filter = request.GET.get('status')
    if status_filter:
        nodes = nodes.filter(status=status_filter)
    # Annotate with latest reading
    node_data = []
    for node in nodes:
        latest = node.sensor_readings.order_by('-timestamp').first()
        node_data.append({'node': node, 'latest': latest})
    return render(request, 'sensors/node_list.html',
                  {'node_data': node_data, 'title': 'Sensor Nodes', 'status_filter': status_filter})


@login_required
def node_detail(request, pk):
    node = get_object_or_404(SensorNode, pk=pk)
    readings = node.sensor_readings.order_by('-timestamp')[:50]
    latest = readings.first() if readings else None
    return render(request, 'sensors/node_detail.html',
                  {'node': node, 'readings': readings, 'latest': latest, 'title': f'Node: {node.node_id}'})


@login_required
def node_create(request):
    form = SensorNodeForm(request.POST or None)
    if form.is_valid():
        node = form.save()
        # Create default sensor sub-types
        TemperatureSensor.objects.create(node=node)
        SmokeSensor.objects.create(node=node)
        FlameSensor.objects.create(node=node)
        HumiditySensor.objects.create(node=node)
        GasSensor.objects.create(node=node)
        messages.success(request, f'Sensor node {node.node_id} created with all sensor types.')
        return redirect('sensors:node_detail', pk=node.pk)
    return render(request, 'sensors/sensor_form.html',
                  {'form': form, 'title': 'Add Sensor Node', 'action': 'Create'})


@login_required
def node_update(request, pk):
    node = get_object_or_404(SensorNode, pk=pk)
    form = SensorNodeForm(request.POST or None, instance=node)
    if form.is_valid():
        form.save()
        messages.success(request, 'Sensor node updated.')
        return redirect('sensors:node_detail', pk=node.pk)
    return render(request, 'sensors/sensor_form.html',
                  {'form': form, 'title': 'Edit Sensor Node', 'action': 'Update', 'object': node})


@login_required
def node_delete(request, pk):
    node = get_object_or_404(SensorNode, pk=pk)
    if request.method == 'POST':
        node.delete()
        messages.success(request, 'Sensor node deleted.')
        return redirect('sensors:node_list')
    return render(request, 'sensors/confirm_delete.html',
                  {'object': node, 'title': 'Delete Sensor Node'})


@login_required
def reading_list(request):
    readings = SensorData.objects.select_related('node__forest_area__forest').order_by('-timestamp')
    condition_filter = request.GET.get('condition')
    risk_filter = request.GET.get('risk')
    if condition_filter:
        readings = readings.filter(condition=condition_filter)
    if risk_filter:
        readings = readings.filter(risk_level=risk_filter)
    paginator = Paginator(readings, 25)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'sensors/reading_list.html',
                  {'page_obj': page_obj, 'title': 'Sensor Readings',
                   'condition_filter': condition_filter, 'risk_filter': risk_filter})


@login_required
def reading_create(request):
    form = SensorDataForm(request.POST or None)
    if form.is_valid():
        reading = form.save(commit=False)
        reading.is_simulated = False
        reading.save()
        messages.success(request, f'Reading recorded. Risk: {reading.risk_level.upper()}, Condition: {reading.condition}.')
        # Auto-generate alert if needed
        if reading.risk_level in ('high', 'critical'):
            _try_generate_alert(reading)
        return redirect('sensors:reading_list')
    return render(request, 'sensors/sensor_form.html',
                  {'form': form, 'title': 'Add Sensor Reading', 'action': 'Record'})


@login_required
def simulate_reading(request, pk):
    """Generate a simulated sensor reading for a node."""
    node = get_object_or_404(SensorNode, pk=pk)
    if request.method == 'POST':
        scenario = request.POST.get('scenario', 'normal')
        reading = _generate_simulated_reading(node, scenario)
        node.last_seen = timezone.now()
        node.save(update_fields=['last_seen'])
        if reading.risk_level in ('high', 'critical'):
            _try_generate_alert(reading)
        messages.success(
            request,
            f'[SIMULATED] Reading recorded — Risk: {reading.risk_level.upper()}, '
            f'Condition: {reading.condition}, Score: {reading.fire_risk_score}'
        )
        return redirect('sensors:node_detail', pk=node.pk)
    return render(request, 'sensors/simulate_form.html',
                  {'node': node, 'title': f'Simulate Reading — {node.node_id}'})


def _generate_simulated_reading(node, scenario='normal'):
    """Create realistic simulated sensor values based on scenario."""
    scenarios = {
        'normal': {
            'temp': (20, 35), 'humidity': (50, 80), 'smoke': (10, 80),
            'gas': (10, 60), 'flame': False, 'intensity': 0,
        },
        'warning': {
            'temp': (38, 52), 'humidity': (25, 45), 'smoke': (100, 220),
            'gas': (70, 140), 'flame': False, 'intensity': 0,
        },
        'fire_suspected': {
            'temp': (55, 72), 'humidity': (12, 28), 'smoke': (250, 420),
            'gas': (150, 250), 'flame': random.random() > 0.5, 'intensity': random.uniform(20, 55),
        },
        'fire_detected': {
            'temp': (75, 110), 'humidity': (5, 18), 'smoke': (450, 700),
            'gas': (250, 450), 'flame': True, 'intensity': random.uniform(60, 100),
        },
    }
    s = scenarios.get(scenario, scenarios['normal'])
    temp = round(random.uniform(*s['temp']), 2)
    humidity = round(random.uniform(*s['humidity']), 2)
    smoke = round(random.uniform(*s['smoke']), 2)
    gas = round(random.uniform(*s['gas']), 2)
    flame = s['flame']
    intensity = round(s['intensity'], 2) if flame else None

    reading = SensorData(
        node=node,
        temperature=Decimal(str(temp)),
        humidity=Decimal(str(humidity)),
        smoke_level=Decimal(str(smoke)),
        gas_concentration=Decimal(str(gas)),
        flame_detected=flame,
        flame_intensity=Decimal(str(intensity)) if intensity else None,
        is_simulated=True,
        notes=f'Auto-simulated: scenario={scenario}',
    )
    reading.save()  # triggers calculate_risk() in model save()
    return reading


def _try_generate_alert(reading):
    """Attempt to create an alert for a high-risk reading."""
    try:
        from alerts.models import Alert
        # Only create one alert per node per hour to avoid spam
        from django.utils import timezone
        import datetime
        one_hour_ago = timezone.now() - datetime.timedelta(hours=1)
        recent = Alert.objects.filter(
            sensor_node=reading.node,
            created_at__gte=one_hour_ago
        ).exists()
        if not recent:
            area = reading.node.forest_area
            Alert.objects.create(
                forest_area=area,
                sensor_node=reading.node,
                trigger_data=reading,
                severity='critical' if reading.condition == 'fire_detected' else
                          'critical' if reading.condition == 'fire_suspected' else 'warning',
                title=f'{reading.get_condition_display()} at {area}' if area else
                      f'{reading.get_condition_display()} — Node {reading.node.node_id}',
                message=(
                    f'Sensor node {reading.node.node_id} reported a {reading.get_condition_display()} '
                    f'condition. Risk Score: {reading.fire_risk_score}/100. '
                    f'Temp: {reading.temperature}°C, Smoke: {reading.smoke_level}ppm, '
                    f'Flame: {"YES" if reading.flame_detected else "No"}. '
                    f'{"[SIMULATED DATA]" if reading.is_simulated else ""}'
                ),
                fire_risk_score=reading.fire_risk_score,
                condition=reading.condition,
                is_simulated=reading.is_simulated,
            )
    except Exception:
        pass  # Alert generation is best-effort
