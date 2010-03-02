from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^update_coords/(?P<entity_type>\w+)$', 'common.views.update_coords'),
)