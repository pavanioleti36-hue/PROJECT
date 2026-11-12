"""Accounts app forms."""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser


# ─── Department choices (used in Register + Profile forms) ───────────────────
DEPARTMENT_CHOICES = [
    ('', '-- Select Department --'),
    # Administration
    ('IT Administration',          'IT Administration'),
    ('System Administration',      'System Administration'),
    # Forest & Environment
    ('Forest Range Department',    'Forest Range Department'),
    ('Forest Conservation',        'Forest Conservation'),
    ('Wildlife Management',        'Wildlife Management'),
    ('Environment Protection',     'Environment Protection'),
    ('Biodiversity Department',    'Biodiversity Department'),
    # Fire & Safety
    ('Fire Department',            'Fire Department'),
    ('Fire Safety & Prevention',   'Fire Safety & Prevention'),
    ('Disaster Management',        'Disaster Management'),
    ('Emergency Response Unit',    'Emergency Response Unit'),
    # Government / Authority
    ('Local Government Authority', 'Local Government Authority'),
    ('Revenue Department',         'Revenue Department'),
    ('District Administration',    'District Administration'),
    ('Panchayat Administration',   'Panchayat Administration'),
    # Technical
    ('Remote Sensing & GIS',       'Remote Sensing & GIS'),
    ('IoT & Sensor Operations',    'IoT & Sensor Operations'),
    ('Data Analytics',             'Data Analytics'),
    # Other
    ('Research & Development',     'Research & Development'),
    ('Training & Education',       'Training & Education'),
    ('Other',                      'Other'),
]


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        })
    )


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=30, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'})
    )
    phone_number = forms.CharField(
        max_length=15, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. +91-9876543210'})
    )
    department = forms.ChoiceField(
        choices=DEPARTMENT_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    employee_id = forms.CharField(
        max_length=20, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Employee / Badge ID'})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'role',
                  'phone_number', 'department', 'employee_id', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})


class ProfileUpdateForm(forms.ModelForm):
    department = forms.ChoiceField(
        choices=DEPARTMENT_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'department',
                  'employee_id', 'profile_picture']
        widgets = {
            'first_name':      forms.TextInput(attrs={'class': 'form-control'}),
            'last_name':       forms.TextInput(attrs={'class': 'form-control'}),
            'email':           forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number':    forms.TextInput(attrs={'class': 'form-control'}),
            'employee_id':     forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }
