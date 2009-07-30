from django.conf.urls.defaults import *


urlpatterns = patterns('',
    (r'^$', 'groups.views.home'),
    (r'^group/is_in_group/$', 'groups.views.is_in_group'),
    (r'^group/join_group/$', 'groups.views.join_group'),
    (r'^group/leave_group/$', 'groups.views.leave_group'),
)
