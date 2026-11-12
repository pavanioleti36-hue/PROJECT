"""
Accounts app models — CustomUser with role-based access.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Extended user model with role-based access control."""

    ROLE_CHOICES = [
        ('administrator', 'Administrator'),
        ('forest_officer', 'Forest Officer'),
        ('fire_department', 'Fire Department'),
        ('local_authority', 'Local Authority'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='forest_officer')
    phone_number = models.CharField(max_length=15, blank=True)
    department = models.CharField(max_length=100, blank=True)
    employee_id = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

    @property
    def is_admin(self):
        return self.role == 'administrator' or self.is_superuser

    @property
    def is_forest_officer(self):
        return self.role == 'forest_officer'

    @property
    def is_fire_dept(self):
        return self.role == 'fire_department'

    @property
    def is_local_authority(self):
        return self.role == 'local_authority'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
