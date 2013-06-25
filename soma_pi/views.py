from django.shortcuts import render_to_response, get_object_or_404
import mpd
import logging

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.utils import simplejson

from soma_pi.models import Station
from soma_pi.forms import StationForm

logger = logging.getLogger(__name__)

def home(request):
    return render_to_response('index.html', 
                              { 'stations': Station.objects.all().order_by('-play_count'),
                                'form': StationForm() },
                              context_instance=RequestContext(request))

def new(request):
    if request.method == 'POST':
        form = StationForm(request.POST)
        if form.is_valid():
            new_station = form.save()
    return HttpResponseRedirect(reverse('home'))

def delete(request,station_id):
    station = get_object_or_404(Station, pk=station_id)
    station.delete()
    return HttpResponseRedirect(reverse('home'))
    
def play(request,station_id):
    # Interact with media player
    station = get_object_or_404(Station, pk=station_id)
    station.play_count = station.play_count + 1;
    station.save()
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
    if method == 'delete':
        return_data = ajax_delete(int(request.GET['station_id']))
    elif method == 'new':
        pass
        
    if return_data:
        return HttpResponse(simplejson.dumps(return_data), 'application/javascript')

    try:
        client = mpd.MPDClient()
        client.connect("localhost", 6600)
    except:
        return_data = {'success': False, 
                       'error': "Could not communicate with MPD",
                       'status': "stop" } 
        return HttpResponse(simplejson.dumps(return_data), 'application/javascript')
    
    if method == 'home':
        return_data = ajax_home_data(client)
    elif method == 'play':
        return_data = ajax_play(client,int(request.GET['station_id']))
    elif method == 'stop':
        return_data = ajax_stop(client)
    elif method == 'playrandom':
        return_data =  ajax_play(client,Station.objects.order_by('?')[0].id)

    client.disconnect()
    return HttpResponse(simplejson.dumps(return_data), 'application/javascript')

def ajax_play(client,station_id):
    try:
        station = Station.objects.get(id=station_id)
        station.play_count = station.play_count + 1;
        station.save()
        client.clear()
        client.add(station.url)
        client.play()
    except:
        return { 'success': False } 
    return {'success': True, 'station': station_id }

def ajax_delete(station_id):
    try:
        station = Station.objects.get(id=station_id)
        station.delete()
    except:
        return {'success':False}
    return {'success': True}

def ajax_stop(client):
    try:
        client.stop()
        client.clear()
    except:
        return { 'success': False } 
    return {'success': True }

def ajax_home_data(client):
    try:
        cs = client.currentsong()
        song = cs['title'] if 'title' in cs else 'Loading...'
        if 'file' not in cs: raise
        name = cs['name']
    except:
        return {'success': True, 
                'status': client.status()['state'] } 

    status = client.status()

    return {'success': True, 
            'status': status['state'],
            'station': name.replace('[SomaFM]','').strip(),
            'song': song } 

    
