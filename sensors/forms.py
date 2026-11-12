"""Sensors app forms."""
from django import forms
from .models import SensorNode, SensorData


class SensorNodeForm(forms.ModelForm):
    class Meta:
        model = SensorNode
        fields = ['node_id', 'name', 'forest_area', 'latitude', 'longitude',
                  'altitude_m', 'status', 'battery_level', 'notes', 'is_simulated']
        widgets = {
            'node_id': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'forest_area': forms.Select(attrs={'class': 'form-select'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0000001'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0000001'}),
            'altitude_m': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'battery_level': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_simulated': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class SensorDataForm(forms.ModelForm):
    class Meta:
        model = SensorData
        fields = ['node', 'temperature', 'humidity', 'smoke_level',
                  'gas_concentration', 'flame_detected', 'flame_intensity', 'notes']
        widgets = {
            'node': forms.Select(attrs={'class': 'form-select'}),
            'temperature': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'humidity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'smoke_level': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'gas_concentration': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'flame_detected': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'flame_intensity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': 0, 'max': 100}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
