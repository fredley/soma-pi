from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'soma_pi.views.home', name='home'),
    url(r'^play/(?P<playlist_no>\d+)/$', 'soma_pi.views.play', name='play'),
    url(r'^stop/$', 'soma_pi.views.stop', name='stop'),
    url(r'^admin/', include(admin.site.urls)),
)
