from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',

    url(r'^$', 
        'feedback.views.index', 
        name="feedback"),

    url(r'^thanks/$', 
        direct_to_template, 
        {'template': 'feedback/feedback_thanks.html'}, 
        name="feedback_thanks"),
)
