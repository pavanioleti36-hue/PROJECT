"""Response management views."""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import EmergencyResponse, FireSuppression, EvacuationManagement, RescueOperation, ResourceAllocation
from .forms import (EmergencyResponseForm, FireSuppressionForm, EvacuationForm,
                    RescueOperationForm, ResourceAllocationForm)
from incidents.models import FireIncident


@login_required
def response_list(request):
    responses = EmergencyResponse.objects.select_related('incident').order_by('-dispatched_at')
    incident_filter = request.GET.get('incident')
    if incident_filter:
        responses = responses.filter(incident_id=incident_filter)
    suppressions = FireSuppression.objects.select_related('incident').order_by('-started_at')[:10]
    evacuations = EvacuationManagement.objects.select_related('incident').order_by('-started_at')[:10]
    return render(request, 'response_mgmt/response_list.html',
                  {'responses': responses, 'suppressions': suppressions,
                   'evacuations': evacuations, 'title': 'Emergency Response'})


@login_required
def response_create(request):
    form = EmergencyResponseForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Emergency response recorded.')
        return redirect('response_mgmt:response_list')
    return render(request, 'response_mgmt/response_form.html',
                  {'form': form, 'title': 'Add Emergency Response', 'action': 'Create'})


@login_required
def response_update(request, pk):
    obj = get_object_or_404(EmergencyResponse, pk=pk)
    form = EmergencyResponseForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Response updated.')
        return redirect('response_mgmt:response_list')
    return render(request, 'response_mgmt/response_form.html',
                  {'form': form, 'title': 'Edit Response', 'action': 'Update', 'object': obj})


@login_required
def response_delete(request, pk):
    obj = get_object_or_404(EmergencyResponse, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Response record deleted.')
        return redirect('response_mgmt:response_list')
    return render(request, 'response_mgmt/confirm_delete.html',
                  {'object': obj, 'title': 'Delete Response'})


# ── Fire Suppression ──────────────────────────────────────────────
@login_required
def suppression_create(request):
    form = FireSuppressionForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Fire suppression record added.')
        return redirect('response_mgmt:response_list')
    return render(request, 'response_mgmt/response_form.html',
                  {'form': form, 'title': 'Add Fire Suppression', 'action': 'Create'})


# ── Evacuation ────────────────────────────────────────────────────
@login_required
def evacuation_create(request):
    form = EvacuationForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Evacuation record added.')
        return redirect('response_mgmt:response_list')
    return render(request, 'response_mgmt/response_form.html',
                  {'form': form, 'title': 'Add Evacuation', 'action': 'Create'})


# ── Rescue Operation ──────────────────────────────────────────────
@login_required
def rescue_create(request):
    form = RescueOperationForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Rescue operation added.')
        return redirect('response_mgmt:response_list')
    return render(request, 'response_mgmt/response_form.html',
                  {'form': form, 'title': 'Add Rescue Operation', 'action': 'Create'})


# ── Resource Allocation ───────────────────────────────────────────
@login_required
def resource_create(request):
    form = ResourceAllocationForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Resource allocation added.')
        return redirect('response_mgmt:response_list')
    return render(request, 'response_mgmt/response_form.html',
                  {'form': form, 'title': 'Allocate Resource', 'action': 'Allocate'})
