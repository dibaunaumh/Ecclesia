from django.conf.urls.defaults import *


urlpatterns = patterns('',
    (r'^discussion/(?P<discussion_slug>.*)/$', 'ecclesia.discussions.views.visualize'),
    (r'^get_stories_view_json/(?P<discussion_slug>.*)$', 'ecclesia.discussions.views.get_stories_view_json'),
    (r'^get_visualization_meta_data/$', 'ecclesia.discussions.views.get_visualization_meta_data'),
    #(r'^submit/$', 'ecclesia.discussions.views.submit_story'),
    (r'^add_story/$', 'ecclesia.discussions.views.add_base_story'),
)
