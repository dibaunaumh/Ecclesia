from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^update_presentation/$', 'common.views.update_presentation'),
    (r'^presentation_status/(?P<model_name>.*)/(?P<object_pk>\d+)', 'common.views.presentation_status'),
    (r'^user_can_view_group/(?P<user_profile_pk>.*)/(?P<group_profile_pk>\d+)', 'common.permissions_views.user_can_view_group'),
    url(r'^lost_password', 'common.views.lost_password', name = 'lost_password'),
    url(r'^change_password/(?P<key>.{70})/$', 'common.views.change_password',name = 'change_password'),
)