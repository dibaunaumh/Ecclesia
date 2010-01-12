from django.conf.urls.defaults import *


urlpatterns = patterns('',
    (r'^discussion/(?P<discussion_slug>.*)/$', 'ecclesia.goals.views.visualize'),
    (r'^submit/$', 'ecclesia.discussions.views.submit_story'),
)
