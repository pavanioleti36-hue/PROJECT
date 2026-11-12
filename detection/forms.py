"""Detection app forms."""
from django import forms
from .models import ThresholdConfig


class ThresholdForm(forms.ModelForm):
    class Meta:
        model = ThresholdConfig
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'temp_warning': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'temp_fire_suspected': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'temp_fire_detected': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'smoke_warning': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'smoke_fire_suspected': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'smoke_fire_detected': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'humidity_warning': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'humidity_critical': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'gas_warning': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'gas_fire_suspected': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'score_warning': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'score_fire_suspected': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'score_fire_detected': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
