from django.urls import path
from . import views

# ENSURE THIS IS SPELLED EXACTLY: urlpatterns
urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_roster, name='upload_roster'),
    path('get-winner/', views.get_winner, name='get_winner'),
    path('reset/', views.reset_roster, name='reset_roster'),
]