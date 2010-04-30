from django.conf.urls.defaults import *


urlpatterns = patterns('',
    (r'^discussion/(?P<discussion_slug>.*)/$', 'ecclesia.discussions.views.visualize'),
    (r'^get_stories_view_json/(?P<discussion_slug>.*)$', 'ecclesia.discussions.views.get_stories_view_json'),
    (r'^get_visualization_meta_data/$', 'ecclesia.discussions.views.get_visualization_meta_data'),
    (r'^get_speech_acts_by_story_type/$', 'ecclesia.discussions.views.get_speech_acts_by_story_type'),
    (r'^get_stories_json/$', 'ecclesia.discussions.views.get_stories_json'),
    #(r'^submit/$', 'ecclesia.discussions.views.submit_story'),
    (r'^add_story/$', 'ecclesia.discussions.views.add_base_story'),
    (r'^story/(?P<story_slug>.*)/$', 'ecclesia.discussions.views.story_home'),
    (r'^merge_stories/(?P<story1_slug>.*)/(?P<story2_slug>.*)$', 'ecclesia.discussions.views.merge_stories'),
    (r'^status/(?P<discussion_slug>.*)$', 'ecclesia.discussions.views.status'),
)
