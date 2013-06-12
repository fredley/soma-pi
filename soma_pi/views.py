from django.shortcuts import render_to_response
import mpd

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext

from soma_pi.models import Station

def home(request):
    stations = Station.objects.all()

    template_args = { 'stations': stations }

    try:
        client = mpd.MPDClient()
        client.connect("localhost", 6600)
        cs = client.currentsong()
        template_args['playing_station'] = cs['name']
        template_args['playing_song'] = cs['title'] if 'title' in cs else cs['file']
        template_args['status'] = True
        client.disconnect()
    except:
        template_args['status'] = False
        template_args['status_message'] = "Is MPC installed?"

    return render_to_response('index.html', template_args,
                              context_instance=RequestContext(request))

def play(request,playlist_no):
    # Interact with media player
    try:
        client = mpd.MPDClient()
        client.connect("localhost", 6600)
        client.play(int(playlist_no))
        client.disconnect()
    except:
        pass

    return HttpResponseRedirect(reverse('home'))

def stop(request):
    try:
        client = mpd.MPDClient()
        client.connect("localhost", 6600)
        client.stop()
        client.disconnect()
    except:
        pass

    return HttpResponseRedirect(reverse('home'))
