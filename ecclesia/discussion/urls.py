from django.conf.urls.defaults import *


urlpatterns = patterns('',
    (r'^submit/$', 'ecclesia.discussion.views.submit_story'),
)
