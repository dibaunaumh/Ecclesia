from django.conf.urls.defaults import *

urlpatterns = patterns('voting.views',
    url(r'^get_voting_form$', 'get_voting_form', name='get_voting_form'),
    url(r'^start_voting/(?P<discussion_pk>\d+)$', 'start_voting', name='start_voting'),
    url(r'^end_voting/$', 'end_voting', name='end_voting'),
    url(r'^add_ballot/(?P<discussion_pk>\d+)$', 'add_ballot', name='add_ballot'),
    url(r'^remove_ballot/(?P<discussion_pk>\d+)$', 'remove_ballot', name='remove_ballot'),
    url(r'^get_vote_progress/(?P<discussion_pk>\d+)$', 'get_vote_progress', name='get_vote_progress'),
)