from django.conf.urls.defaults import *


urlpatterns = patterns('discussions.views',
    (r'^discussion/evaluate/(?P<discussion_slug>.*)/$', 'evaluate'),
    (r'^discussion/(?P<discussion_slug>.*)/$', 'visualize'),
    (r'^get_update/(?P<discussion_slug>.*)$', 'get_update'),
#    (r'^get_stories_view_json/(?P<discussion_slug>.*)$', 'get_stories_view_json'),
    (r'^get_visualization_meta_data/$', 'get_visualization_meta_data'),
    (r'^get_hints_meta_data/(?P<discussion_slug>.*)/$', 'get_hints_metadata'),
    (r'^add_discussion/$', 'add_discussion'),
    (r'^add_story/$', 'add_base_story'),
    (r'^delete_story/$', 'delete_story'),
    (r'^delete_story_a/(?P<story_pk>.*)/$', 'delete_story_a'),
    (r'^delete_relation/(?P<relation_pk>.*)/$', 'delete_relation'),
    (r'^delete_opinion/$', 'delete_opinion'),
    (r'^edit_opinion/$', 'edit_opinion'),
    (r'^(?P<discussion_slug>.*)/(?P<ctype>story)/(?P<slug>.*)/$', 'story_home'),
    (r'^(?P<discussion_slug>.*)/(?P<ctype>relation)/(?P<slug>.*)/$', 'story_home'),
    url(r'^save_view/$', 'save_view', name='save_view'),
    (r'^merge_stories/(?P<story1_slug>.*)/(?P<story2_slug>.*)$', 'merge_stories'),
    (r'^get_stories_json_by_speechact/(?P<discussion_pk>\d+)/(?P<speech_act>.*)/$','get_inline_select_json'),
    (r'^edit_inline_select_field/(?P<relation_id>.*)/(?P<direction>.*)/$', 'get_inline_select_field'),
    url(r'^follow/(?P<discussion_slug>.*)/$', 'follow', name='discussion_follow'),
    url(r'^unfollow/(?P<discussion_slug>.*)/$', 'unfollow', name='discussion_unfollow'),

    (r'^im_api/create_discussion/', 'create_discussion_via_im'),
)
