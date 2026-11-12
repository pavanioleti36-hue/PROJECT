"""Incidents app views."""

import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.utils import timezone
from .models import FireIncident, IncidentUpdate
from .forms import FireIncidentForm, IncidentUpdateForm, IncidentSearchForm
from response_mgmt.models import EmergencyResponse


@login_required
def incident_list(request):
    incidents = FireIncident.objects.select_related('forest', 'forest_area').order_by('-fire_start_time')
    form = IncidentSearchForm(request.GET or None)
    if form.is_valid():
        q = form.cleaned_data.get('q')
        severity = form.cleaned_data.get('severity')
        status = form.cleaned_data.get('status')
        if q:
            incidents = incidents.filter(title__icontains=q) | \
                        FireIncident.objects.filter(incident_id__icontains=q)
        if severity:
            incidents = incidents.filter(severity=severity)
        if status:
            incidents = incidents.filter(status=status)
    paginator = Paginator(incidents, 15)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'incidents/incident_list.html',
                  {'page_obj': page_obj, 'form': form, 'title': 'Fire Incidents'})


@login_required
def incident_detail(request, pk):
    incident = get_object_or_404(FireIncident, pk=pk)
    updates = incident.updates.order_by('-updated_at')
    responses = incident.responses.all()
    update_form = IncidentUpdateForm()
    return render(request, 'incidents/incident_detail.html',
                  {'incident': incident, 'updates': updates,
                   'responses': responses, 'update_form': update_form,
                   'title': incident.incident_id})


@login_required
def incident_create(request):
    form = FireIncidentForm(request.POST or None)
    if form.is_valid():
        incident = form.save(commit=False)
        incident.reported_by = request.user
        incident.save()
        messages.success(request, f'Fire incident {incident.incident_id} recorded.')
        return redirect('incidents:incident_detail', pk=incident.pk)
    return render(request, 'incidents/incident_form.html',
                  {'form': form, 'title': 'Report Fire Incident', 'action': 'Report'})


@login_required
def incident_update(request, pk):
    incident = get_object_or_404(FireIncident, pk=pk)
    form = FireIncidentForm(request.POST or None, instance=incident)
    if form.is_valid():
        form.save()
        messages.success(request, 'Incident updated.')
        return redirect('incidents:incident_detail', pk=incident.pk)
    return render(request, 'incidents/incident_form.html',
                  {'form': form, 'title': 'Edit Incident', 'action': 'Update', 'object': incident})


@login_required
def incident_delete(request, pk):
    incident = get_object_or_404(FireIncident, pk=pk)
    if request.method == 'POST':
        incident.delete()
        messages.success(request, 'Incident deleted.')
        return redirect('incidents:incident_list')
    return render(request, 'incidents/confirm_delete.html',
                  {'object': incident, 'title': 'Delete Incident'})


@login_required
def incident_add_update(request, pk):
    incident = get_object_or_404(FireIncident, pk=pk)
    if request.method == 'POST':
        form = IncidentUpdateForm(request.POST)
        if form.is_valid():
            update = form.save(commit=False)
            update.incident = incident
            update.updated_by = request.user
            update.save()
            # Apply status/severity changes to incident
            if update.new_status:
                incident.status = update.new_status
            if update.new_severity:
                incident.severity = update.new_severity
            if update.new_status in ('extinguished', 'false_alarm') and not incident.fire_end_time:
                incident.fire_end_time = timezone.now()
            incident.save()
            messages.success(request, 'Incident update added.')
    return redirect('incidents:incident_detail', pk=pk)


@login_required
def export_incidents_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="fire_incidents.csv"'
    writer = csv.writer(response)
    writer.writerow(['Incident ID', 'Title', 'Forest', 'Forest Area', 'Severity',
                     'Status', 'Start Time', 'End Time', 'Area Burned (ha)',
                     'Location', 'Simulated', 'Reported At'])
    for inc in FireIncident.objects.select_related('forest', 'forest_area').order_by('-fire_start_time'):
        writer.writerow([
            inc.incident_id, inc.title,
            inc.forest.name if inc.forest else '',
            inc.forest_area.name if inc.forest_area else '',
            inc.get_severity_display(), inc.get_status_display(),
            inc.fire_start_time.strftime('%Y-%m-%d %H:%M') if inc.fire_start_time else '',
            inc.fire_end_time.strftime('%Y-%m-%d %H:%M') if inc.fire_end_time else '',
            inc.area_burned_hectares or '',
            inc.location_description,
            'Yes' if inc.is_simulated else 'No',
            inc.reported_at.strftime('%Y-%m-%d %H:%M'),
        ])
    return response
