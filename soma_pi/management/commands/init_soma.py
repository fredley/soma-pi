import urllib2

import xml.etree.ElementTree as ET
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from soma_pi.models import Station

class Command(BaseCommand):
    help = 'Initializes the database with all SomaFM stations'

    option_list = BaseCommand.option_list + (
        make_option('--clear',
            action='store_true',
            dest='clear',
            default=False,
            help='Clear database before adding stations.'),
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing database.')
            for station in Station.objects.all():
                station.delete()
        try:
            xml = urllib2.urlopen("http://api.somafm.com/channels.xml").read()
        except:
            self.stdout.write('Could not connect to somafm.')
            return
        self.stdout.write('Got data from SomaFM')
        try:
            data = ET.fromstring(xml)
        except:
            self.stdout.write('XML could not be parsed.')
            return
        self.stdout.write('Parsed data')
        for channel in data.findall('channel'):
            try:
                pls = urllib2.urlopen(channel.find('fastpls').text).read()
                for line in iter(pls.splitlines()):
                    if line[0:5] == 'File1':
                        stream = line[6:]
                        break
                url = stream # Just to dump us out if stream is not found
            except:
                self.stdout.write('Problem getting url for station: %s' % channel.find('title').text)
                continue

            new_station = Station()
            new_station.name = channel.find('title').text
            new_station.description = channel.find('description').text
            new_station.url = stream
            new_station.image = channel.find('image').text
            new_station.save()
            self.stdout.write('Added station: %s' % new_station.name)
