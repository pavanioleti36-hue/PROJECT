"""Forms for Forest Environment app."""
from django import forms
from .models import Forest, ForestArea, Vegetation, Wildlife, WeatherCondition


class ForestForm(forms.ModelForm):
    class Meta:
        model = Forest
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'established_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_area_hectares': forms.NumberInput(attrs={'class': 'form-control'}),
            'forest_type': forms.TextInput(attrs={'class': 'form-control'}),
            'is_protected': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ForestAreaForm(forms.ModelForm):
    class Meta:
        model = ForestArea
        fields = '__all__'
        widgets = {
            'forest': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'zone_type': forms.Select(attrs={'class': 'form-select'}),
            'area_hectares': forms.NumberInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0000001'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0000001'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_high_risk': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class VegetationForm(forms.ModelForm):
    class Meta:
        model = Vegetation
        fields = '__all__'
        widgets = {
            'forest_area': forms.Select(attrs={'class': 'form-select'}),
            'vegetation_type': forms.TextInput(attrs={'class': 'form-control'}),
            'density': forms.Select(attrs={'class': 'form-select'}),
            'moisture_content': forms.NumberInput(attrs={'class': 'form-control'}),
            'fire_susceptibility': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class WildlifeForm(forms.ModelForm):
    class Meta:
        model = Wildlife
        fields = '__all__'
        widgets = {
            'forest_area': forms.Select(attrs={'class': 'form-select'}),
            'species_name': forms.TextInput(attrs={'class': 'form-control'}),
            'scientific_name': forms.TextInput(attrs={'class': 'form-control'}),
            'population_estimate': forms.NumberInput(attrs={'class': 'form-control'}),
            'conservation_status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class WeatherConditionForm(forms.ModelForm):
    class Meta:
        model = WeatherCondition
        fields = '__all__'
        widgets = {
            'forest_area': forms.Select(attrs={'class': 'form-select'}),
            'temperature': forms.NumberInput(attrs={'class': 'form-control'}),
            'humidity': forms.NumberInput(attrs={'class': 'form-control'}),
            'wind_speed': forms.NumberInput(attrs={'class': 'form-control'}),
            'wind_direction': forms.TextInput(attrs={'class': 'form-control'}),
            'rainfall': forms.NumberInput(attrs={'class': 'form-control'}),
            'condition': forms.TextInput(attrs={'class': 'form-control'}),
            'recorded_at': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
        }
