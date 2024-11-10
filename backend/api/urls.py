# api/urls.py
from django.urls import path
from .views import find_stops_in_danger_tract_view, find_wards_view, all_wards_view

urlpatterns = [
    path('find-stops/', find_stops_in_danger_tract_view, name='find_stops_in_danger_tract'),
    path('find-wards/', find_wards_view, name='find_wards'),
    path('all-wards/', all_wards_view, name='all_wards'),
]