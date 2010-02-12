from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^update_presentation/$', 'common.views.update_presentation'),
)