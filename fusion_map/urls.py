""" fusion_map URL Configuration
"""

from django.urls import path
from main import api, views

urlpatterns = [
    path('', views.index),

    path('api/1/locations/add', api.add_location),
    path('api/1/locations/removeall', api.remove_all),
]
