from django.db import models


class Station(models.Model):
    """ Keeps track of the station URL and its position in the playlist"""

    url = models.CharField(max_length=200)
    position = models.IntegerField()

    def __unicode__(self):
        return "(" + str(position) + ")" + url
