# D:\Projects\RDRealty\RDRealty\urls.py (Your Project's main urls.py)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 1. Admin Interface (Standard Django Path)
    path('admin/', admin.site.urls),

    # 2. Link your RDRealty_App URLs here
    # When a user goes to the root path (''), Django will look in RDRealty_App/urls.py
    path('', include('RDRealty_App.urls')), 

    # 3. Add Django's built-in authentication URLs
    # This includes URLs for login, logout, password change, etc.
    path('accounts/', include('django.contrib.auth.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)