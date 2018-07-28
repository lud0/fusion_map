from django.conf import settings
from django.shortcuts import render

from . import fusion_table
from .models import MapLocation


def index(request):
    """ Index page
    """

    locations = list(MapLocation.objects.all().values_list('address', flat=True))
    context = {
        'GOOGLE_API_KEY': settings.GOOGLE_API_KEY,
        'GOOGLE_FUSIONTABLE_ID': fusion_table.table_id,
        'existing_addresses': locations,
    }

    return render(request, 'index.html', context)
