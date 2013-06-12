from django.db import models


class Station(models.Model):
    """ Keeps track of the station URL and its position in the playlist"""

    url = models.CharField(max_length=60)
    position = models.IntegerField()
    image = models.CharField(max_length=200)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    def __unicode__(self):
        return "(" + str(self.position) + ") " + self.name
