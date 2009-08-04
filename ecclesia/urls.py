from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    (r'^goal/(?P<goal_id>\d+)/visualize/$', 'ecclesia.goals.views.visualize'),
    (r'^goal/(?P<goal_id>\d+)/json/$', 'ecclesia.goals.views.json'),
    (r'^goal/(?P<goal_id>\d+)/stories/$', 'ecclesia.goals.views.stories'),
    (r'^goal/(?P<goal_id>\d+)/courseofaction/create/$', 'ecclesia.goals.views.create_course_of_action'),
    (r'^goal/(?P<goal_id>\d+)/possibleresult/create/$', 'ecclesia.goals.views.create_possible_result'),
        
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
    
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static'}), # serve static content. only for development.

    (r'^', include('ecclesia.groups.urls')),
)
