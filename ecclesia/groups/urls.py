from django.conf.urls.defaults import *


urlpatterns = patterns('',
    (r'^group/is_in_group/$', 'groups.views.is_in_group'),
    (r'^group/join_group/$', 'groups.views.join_group'),
    (r'^group/leave_group/$', 'groups.views.leave_group'),
    (r'^group/(?P<group_name>.*)/$', 'groups.views.group_home'),
    (r'^users/(?P<user_name>.*)/$', 'groups.views.user_home'),
    (r'^$', 'groups.views.home'),
)
