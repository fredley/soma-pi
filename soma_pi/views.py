from django.shortcuts import render_to_response, get_object_or_404
import mpd
import logging

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.utils import simplejson

from soma_pi.models import Station

logger = logging.getLogger(__name__)

def home(request):
    return render_to_response('index.html', 
                              { 'stations': Station.objects.all() },
                              context_instance=RequestContext(request))

def play(request,station_id):
    # Interact with media player
    station = get_object_or_404(Station, pk=station_id)
    try:
        client = mpd.MPDClient()
        client.connect("localhost", 6600)
        client.clear()
        client.add(station.url)
        client.play()
        client.disconnect()
    except:
        pass

    return HttpResponseRedirect(reverse('home'))

def random(request):
    return HttpResponseRedirect(reverse('play',args=[Station.objects.order_by('?')[0].id]))

def stop(request):
    try:
        client = mpd.MPDClient()
        client.connect("localhost", 6600)
        client.clear()
        client.stop()
        client.disconnect()
    except:
        pass

    return HttpResponseRedirect(reverse('home'))

def ajax(request,method):
    if method == 'home':
        return_data = ajax_home_data()

    return HttpResponse(simplejson.dumps(return_data), 'application/javascript')

def ajax_home_data():
    try:
        client = mpd.MPDClient()
        client.connect("localhost", 6600)
    except:
        return {'success': False, 
                'error': "Could not communicate with MPD",
                'status': "stop" } 

    try:
        cs = client.currentsong()
        logger.debug(cs)
        song = cs['title'] if 'title' in cs else 'Loading...'
        if 'file' not in cs: raise
        name = cs['name']
    except:
        return {'success': True, 
                'status': client.status()['state'] } 

    status = client.status()

    client.disconnect()

    return {'success': True, 
            'status': status['state'],
            'station': name.replace('[SomaFM]','').strip(),
            'song': song } 

    
