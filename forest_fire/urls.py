"""URL configuration for forest_fire project."""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('reports.urls')),
    path('forest/', include('forest_env.urls')),
    path('sensors/', include('sensors.urls')),
    path('detection/', include('detection.urls')),
    path('alerts/', include('alerts.urls')),
    path('incidents/', include('incidents.urls')),
    path('response/', include('response_mgmt.urls')),
    path('', lambda request: redirect('dashboard:home'), name='root'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom admin site header
admin.site.site_header = "Forest Fire Detection System"
admin.site.site_title = "FFDS Admin"
admin.site.index_title = "System Administration"
