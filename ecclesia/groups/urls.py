from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^group/is_in_group/$', 'groups.views.is_in_group'),
    (r'^group/join_group/$', 'groups.views.join_group'),
    (r'^group/leave_group/$', 'groups.views.leave_group'),
    (r'^group/(?P<group_name>.*)/$', 'groups.views.group_home'),
    (r'^group-delete/(?P<group_pk>.*)/$', 'groups.views.delete_group'),
    (r'^member-delete/(?P<group_pk>\w+)/(?P<member_pk>\w+)/$', 'groups.views.delete_member'),
    (r'^member-promote/(?P<group_pk>\w+)/(?P<member_pk>\w+)/$', 'groups.views.promote_member'),
    (r'^member-demote/(?P<group_pk>\w+)/(?P<member_pk>\w+)/$', 'groups.views.demote_member'),
    (r'^users/(?P<user_name>.*)/$', 'groups.views.user_home'),
    (r'^$', 'groups.views.home'),
    (r'^groupslist/$', 'groups.views.groups_list'),
    #(r'^login/$', 'groups.views.login'),
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}),
)
