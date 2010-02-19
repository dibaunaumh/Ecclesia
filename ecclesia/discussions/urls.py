from django.conf.urls.defaults import *


urlpatterns = patterns('',
    (r'^(?P<discussion_slug>.*)/$', 'ecclesia.discussions.views.visualize'),
    (r'^get_stories_view_json/(?P<discussion_slug>.*)$', 'ecclesia.discussions.views.get_stories_view_json'),
    #(r'^submit/$', 'ecclesia.discussions.views.submit_story'),
)
