from django.db import models
from . import fusion_table


class MapLocation(models.Model):
    """
    Location model
    """

    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=200, null=True)

    def __unicode__(self):
        return '{0} ({1}, {2})'.format(self.address, self.latitude, self.longitude)

    def fusion_exists(self):
        return fusion_table.location_exists(self.latitude, self.longitude)

    def local_exists(self):
        return self.__class__.objects.filter(latitude=self.latitude, longitude=self.longitude).exists()

    def create(self):
        self.save()
        fusion_table.add_location(self.address, self.latitude, self.longitude)
