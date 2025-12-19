# new_roullette/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('fishing_roullette.urls')), # This tells Django to look at your app
]
