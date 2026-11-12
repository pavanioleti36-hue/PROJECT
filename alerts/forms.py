"""Alerts app forms."""
from django import forms
from .models import Alert


class AlertForm(forms.ModelForm):
    class Meta:
        model = Alert
        fields = ['forest_area', 'sensor_node', 'severity', 'title', 'message', 'condition']
        widgets = {
            'forest_area': forms.Select(attrs={'class': 'form-select'}),
            'sensor_node': forms.Select(attrs={'class': 'form-select'}),
            'severity': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'condition': forms.Select(attrs={'class': 'form-select'},
                                      choices=[('', '-- Select --'),
                                               ('normal', 'Normal'),
                                               ('warning', 'Warning'),
                                               ('fire_suspected', 'Fire Suspected'),
                                               ('fire_detected', 'Fire Detected')]),
        }
