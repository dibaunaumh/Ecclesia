from django.conf.urls.defaults import *


urlpatterns = patterns('',
    (r'^(?P<goal_id>\d+)/visualize/$', 'ecclesia.goals.views.visualize'),
    (r'^(?P<goal_id>\d+)/json/$', 'ecclesia.goals.views.json'),
    (r'^(?P<goal_id>\d+)/stories/$', 'ecclesia.goals.views.stories'),
    (r'^(?P<goal_id>\d+)/courseofaction/create/$', 'ecclesia.goals.views.create_course_of_action'),
    (r'^(?P<goal_id>\d+)/possibleresult/create/$', 'ecclesia.goals.views.create_possible_result'),
)

