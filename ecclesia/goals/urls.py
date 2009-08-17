from django.conf.urls.defaults import *


urlpatterns = patterns('',
    (r'^(?P<goal_id>\d+)/visualize/$', 'ecclesia.goals.views.visualize'),
    (r'^(?P<goal_id>\d+)/data/$', 'ecclesia.goals.views.get_path_resolution_data'),
    (r'^(?P<goal_id>\d+)/stories/$', 'ecclesia.goals.views.stories'),
    (r'^(?P<goal_id>\d+)/stories/write/$', 'ecclesia.goals.views.write_story'),
    (r'^(?P<goal_id>\d+)/courseofaction/create/$', 'ecclesia.goals.views.create_course_of_action'),
    (r'^(?P<goal_id>\d+)/possibleresult/create/$', 'ecclesia.goals.views.create_possible_result'),
)

