from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^end_voting/$', 'voting.views.end_voting', name='end_voting'),
    url(r'^add_ballot/(?P<discussion_pk>\d+)/(?P<story_pk>\d+)', 'voting.views.add_ballot', name='add_ballot'),
    url(r'^remove_ballot/(?P<discussion_pk>\d+)/(?P<story_pk>\d+)', 'voting.views.remove_ballot', name='remove_ballot'),   
)