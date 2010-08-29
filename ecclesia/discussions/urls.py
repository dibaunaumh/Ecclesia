from django.conf.urls.defaults import *


urlpatterns = patterns('',
    (r'^discussion/evaluate/(?P<discussion_slug>.*)/$', 'ecclesia.discussions.views.evaluate'),    
    (r'^discussion/(?P<discussion_slug>.*)/$', 'ecclesia.discussions.views.visualize'),
    (r'^get_stories_view_json/(?P<discussion_slug>.*)$', 'ecclesia.discussions.views.get_stories_view_json'),
    (r'^get_visualization_meta_data/$', 'ecclesia.discussions.views.get_visualization_meta_data'),
    (r'^get_stories_json/$', 'ecclesia.discussions.views.get_stories_json'),
    #(r'^submit/$', 'ecclesia.discussions.views.submit_story'),
    (r'^add_discussion/$', 'ecclesia.discussions.views.add_discussion'),
    (r'^add_story/$', 'ecclesia.discussions.views.add_base_story'),
    (r'^delete_story/(?P<story_pk>.*)/$', 'discussions.views.delete_story'),
    (r'^delete_relation/(?P<relation_pk>.*)/$', 'discussions.views.delete_relation'),
    (r'^(?P<discussion_slug>.*)/(?P<ctype>story)/(?P<slug>.*)/$', 'ecclesia.discussions.views.story_home'),
    (r'^(?P<discussion_slug>.*)/(?P<ctype>relation)/(?P<slug>.*)/$', 'ecclesia.discussions.views.story_home'),
    (r'^merge_stories/(?P<story1_slug>.*)/(?P<story2_slug>.*)$', 'ecclesia.discussions.views.merge_stories'),
    (r'^status/(?P<discussion_slug>.*)$', 'ecclesia.discussions.views.status'),
    (r'^get_stories_json_by_speechact/(?P<discussion_pk>\d+)/(?P<speech_act>.*)/$','ecclesia.discussions.views.get_inline_select_json'),
    (r'^edit_inline_select_field/(?P<relation_id>.*)/(?P<direction>.*)/$', 'ecclesia.discussions.views.get_inline_select_field'),
    (r'^follow/(?P<discussion_slug>.*)/$', 'ecclesia.discussions.views.follow'),
)
