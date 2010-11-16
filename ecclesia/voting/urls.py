from django.conf.urls.defaults import *

urlpatterns = patterns('voting.views',
    url(r'^get_voting_form$', 'get_voting_form'),
    url(r'^start_voting/(?P<discussion_pk>\d+)$', 'start_voting'),
    url(r'^end_voting/$', 'end_voting', name='end_voting'),
    url(r'^add_ballot/(?P<discussion_pk>\d+)$', 'add_ballot', name='add_ballot'),
    url(r'^remove_ballot/(?P<discussion_pk>\d+)/(?P<story_pk>\d+)', 'remove_ballot', name='remove_ballot'),
)