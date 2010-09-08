from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^update_presentation/$', 'common.views.update_presentation'),
    (r'^presentation_status/(?P<model_name>.*)/(?P<object_pk>\d+)', 'common.views.presentation_status'),
)