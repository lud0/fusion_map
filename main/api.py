from django.http import JsonResponse

from . import fusion_table
from .models import MapLocation


def add_location(request):
    """ Add a new location both locally and on fusion table provided it isn't a duplicated entry
    """

    lat = request.POST.get('lat', None)
    lng = request.POST.get('lng', None)
    address = request.POST.get('address', None)

    if lat and lng and address:

        location = MapLocation(latitude=lat,
                               longitude=lng,
                               address=address)

        if location.local_exists() or location.fusion_exists():
            data = {'result': 'Location already added'}
        else:
            location.create()
            data = {'result': 'ok'}
    else:
        data = {'result': 'Missing some values'}

    return JsonResponse(data)


def remove_all(request):
    """ Remove all locations from local db and fusion table
    """

    # Remove local db locations
    MapLocation.objects.all().delete()

    # Remove remote fusion db locations
    fusion_table.remove_all()

    data = {'result': 'ok'}
    return JsonResponse(data)
