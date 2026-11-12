"""Incidents app forms."""
from django import forms
from .models import FireIncident, IncidentUpdate


class FireIncidentForm(forms.ModelForm):
    class Meta:
        model = FireIncident
        fields = ['forest', 'forest_area', 'title', 'description', 'latitude', 'longitude',
                  'location_description', 'severity', 'status', 'fire_start_time',
                  'fire_end_time', 'area_burned_hectares', 'estimated_damage']
        widgets = {
            'forest': forms.Select(attrs={'class': 'form-select'}),
            'forest_area': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0000001'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0000001'}),
            'location_description': forms.TextInput(attrs={'class': 'form-control'}),
            'severity': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'fire_start_time': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'fire_end_time': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'area_burned_hectares': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'estimated_damage': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class IncidentUpdateForm(forms.ModelForm):
    class Meta:
        model = IncidentUpdate
        fields = ['update_text', 'new_status', 'new_severity']
        widgets = {
            'update_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,
                                                  'placeholder': 'Describe the update...'}),
            'new_status': forms.Select(attrs={'class': 'form-select'}),
            'new_severity': forms.Select(attrs={'class': 'form-select'}),
        }


class IncidentSearchForm(forms.Form):
    q = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Search by title, ID...'}))
    severity = forms.ChoiceField(required=False, choices=[('', 'All Severities')] +
                                  FireIncident.SEVERITY_CHOICES,
                                  widget=forms.Select(attrs={'class': 'form-select'}))
    status = forms.ChoiceField(required=False, choices=[('', 'All Statuses')] +
                                FireIncident.STATUS_CHOICES,
                                widget=forms.Select(attrs={'class': 'form-select'}))
