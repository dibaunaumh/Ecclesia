from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',



    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #(r'^admin/', include(admin.site.urls)),
    (r'^admin/(.*)', admin.site.root),

    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static'}), # serve static content. only for development.

    (r'^invites/', include('privatebeta.urls')),

    #(r'^story/', include('ecclesia.discussions.urls')),

    (r'^discussions/', include('ecclesia.discussions.urls')),
    (r'^common/', include('ecclesia.common.urls')),
    #(r'^accounts/', include('registration.urls')),
    (r'accounts/', include('registration.urls')),

    (r'^', include('ecclesia.groups.urls')),
    (r'^edit_inline/$', 'ecclesia.discussions.views.get_inline_field'),
    (r'^i18n/', include('django.conf.urls.i18n')),
)
