from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext

from soma_pi.models import Station

def home(request):
    stations = Station.objects.all()
    return render_to_response('index.html',{'stations': stations},
                              context_instance=RequestContext(request))

def play(request,playlist_no):
    # Interact with media player
    return HttpResponseRedirect(reverse('home'))
