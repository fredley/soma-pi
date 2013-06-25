from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'soma_pi.views.home', name='home'),
    url(r'^play/(?P<station_id>\d+)/$', 'soma_pi.views.play', name='play'),
    url(r'^stop/$', 'soma_pi.views.stop', name='stop'),
    url(r'^new/$', 'soma_pi.views.new', name='new'),
    url(r'^random/$', 'soma_pi.views.random', name='random'),
    url(r'^ajax/(?P<method>\w+)/$', 'soma_pi.views.ajax', name='ajax'),
    url(r'^admin/', include(admin.site.urls)),
)
