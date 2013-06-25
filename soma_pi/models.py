from django.db import models


class Station(models.Model):
    """ Keeps track of the station URL and details """

    url = models.CharField(max_length=300)
    image = models.CharField(max_length=200)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    play_count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name
