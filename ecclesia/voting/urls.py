from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^end_voting/$', 'voting.views.end_voting', name='end_voting'),
)