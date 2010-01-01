from django.conf.urls.defaults import *


urlpatterns = patterns('',
    (r'^submit/$', 'ecclesia.discussions.views.submit_story'),
)
