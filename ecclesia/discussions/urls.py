from django.conf.urls.defaults import *


urlpatterns = patterns('',
    (r'^(?P<discussion_slug>.*)/$', 'ecclesia.discussions.views.visualize'),
    #(r'^submit/$', 'ecclesia.discussions.views.submit_story'),
)
