from django.contrib.gis.db import models


class Crashes(models.Model):
    hour = models.IntegerField(default=-1)
    mode = models.CharField(max_length=10)
    geometry = models.PointField(srid=4326, null=True)

    def __str__(self):
        return "hour: " + str(self.hour) + ", " + "mode: " + str(self.mode) \
               + ", coordinates: " + str(self.geometry)


class DriveNetwork(models.Model):
    start = models.CharField(max_length=20)
    end = models.CharField(max_length=20)
    geometry = models.LineStringField(srid=4326, null=True)

    def __str__(self):
        return "drive network -> " + "start: " + str(self.start) + ", end: " + str(self.end)


class DriveNodes(models.Model):
    osmid = models.CharField(max_length=20)
    geometry = models.PointField(srid=4326, null=True)

    def __str__(self):
        return "drive node: " + str(self.osmid)
