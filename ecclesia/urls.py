from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',



    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static'}), # serve static content. only for development.

    (r'^invites/', include('privatebeta.urls')),

    #(r'^story/', include('ecclesia.discussions.urls')),

    (r'^discussions/', include('ecclesia.discussions.urls')),
    (r'^voting/', include('ecclesia.voting.urls')),
    (r'^common/', include('ecclesia.common.urls')),
    (r'^accounts/', include('registration.urls')),
    (r'^accounts/', include('socialauth.urls')),
    (r'^feedback/', include('feedback.urls')),

    (r'^', include('ecclesia.groups.urls')),
    (r'^edit_inline/$', 'ecclesia.discussions.views.get_inline_field'),
    (r'^i18n/', include('django.conf.urls.i18n')),


)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )
