from django.conf.urls.defaults import *


urlpatterns = patterns('',
    (r'^group/is_in_group/$', 'groups.views.is_in_group'),
    (r'^group/join_group/$', 'groups.views.join_group'),
    (r'^group/leave_group/$', 'groups.views.leave_group'),
    (r'^group/(?P<group_name>.*)/$', 'groups.views.group_home'),
    (r'^users/(?P<user_name>.*)/$', 'groups.views.user_home'),
    (r'^$', 'groups.views.home'),
    (r'^groupslist/$', 'groups.views.groups_list'),
    (r'^update_coords/$', 'groups.views.update_coords'),
    #(r'^login/$', 'groups.views.login'),
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}),
)
