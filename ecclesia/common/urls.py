from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^update_presentation/$', 'common.views.update_presentation'),
    (r'^presentation_status/(?P<model_name>.*)/(?P<object_pk>\d+)', 'common.views.presentation_status'),
    (r'^user_can_view_group/(?P<user_profile_pk>.*)/(?P<group_profile_pk>\d+)', 'common.permissions_views.user_can_view_group'),
)