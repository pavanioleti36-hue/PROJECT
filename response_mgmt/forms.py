"""Response management forms."""
from django import forms
from .models import EmergencyResponse, FireSuppression, EvacuationManagement, RescueOperation, ResourceAllocation


class EmergencyResponseForm(forms.ModelForm):
    class Meta:
        model = EmergencyResponse
        fields = ['incident', 'response_team', 'response_leader', 'status',
                  'dispatched_at', 'arrived_at', 'completed_at', 'personnel_count', 'vehicles', 'notes']
        widgets = {
            'incident': forms.Select(attrs={'class': 'form-select'}),
            'response_team': forms.TextInput(attrs={'class': 'form-control'}),
            'response_leader': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'dispatched_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'arrived_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'completed_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'personnel_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'vehicles': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class FireSuppressionForm(forms.ModelForm):
    class Meta:
        model = FireSuppression
        fields = ['incident', 'method', 'resources_used', 'water_used_liters',
                  'started_at', 'completed_at', 'effectiveness', 'notes']
        widgets = {
            'incident': forms.Select(attrs={'class': 'form-select'}),
            'method': forms.TextInput(attrs={'class': 'form-control'}),
            'resources_used': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'water_used_liters': forms.NumberInput(attrs={'class': 'form-control'}),
            'started_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'completed_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'effectiveness': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class EvacuationForm(forms.ModelForm):
    class Meta:
        model = EvacuationManagement
        fields = ['incident', 'evacuation_zone', 'people_evacuated', 'evacuation_route',
                  'shelter_location', 'started_at', 'completed_at', 'coordinator', 'notes']
        widgets = {
            'incident': forms.Select(attrs={'class': 'form-select'}),
            'evacuation_zone': forms.TextInput(attrs={'class': 'form-control'}),
            'people_evacuated': forms.NumberInput(attrs={'class': 'form-control'}),
            'evacuation_route': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'shelter_location': forms.TextInput(attrs={'class': 'form-control'}),
            'started_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'completed_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'coordinator': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class RescueOperationForm(forms.ModelForm):
    class Meta:
        model = RescueOperation
        fields = ['incident', 'operation_name', 'people_rescued', 'people_missing',
                  'rescue_team', 'started_at', 'completed_at', 'status', 'notes']
        widgets = {
            'incident': forms.Select(attrs={'class': 'form-select'}),
            'operation_name': forms.TextInput(attrs={'class': 'form-control'}),
            'people_rescued': forms.NumberInput(attrs={'class': 'form-control'}),
            'people_missing': forms.NumberInput(attrs={'class': 'form-control'}),
            'rescue_team': forms.TextInput(attrs={'class': 'form-control'}),
            'started_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'completed_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class ResourceAllocationForm(forms.ModelForm):
    class Meta:
        model = ResourceAllocation
        fields = ['incident', 'resource_type', 'resource_name', 'quantity', 'unit', 'status', 'notes']
        widgets = {
            'incident': forms.Select(attrs={'class': 'form-select'}),
            'resource_type': forms.Select(attrs={'class': 'form-select'}),
            'resource_name': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
