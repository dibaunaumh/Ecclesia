# This Python file uses the following encoding: utf-8
from ecclesia.goals.models import *
from ecclesia.operations.models import *

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.http import HttpResponse


def visualize(request,goal_id):
    g = get_object_or_404(Goal, pk=goal_id)
    context = dict()
    context['goal'] = g
    return render_to_response('visualize_canvas.html', {'context':context})

def json(request,goal_id):
    g = get_object_or_404(Goal, pk=goal_id)
    res = u"""{"goal": {"id": %d, "name": "%s","short_description": "%s", "storiesURL":"/goal/%d/stories/" },     
              "actions": [{"id":1,"name":"a1","storiesURL":"/stories/"},{"id":2,"name":"action2","storiesURL":"/stories/"},{"id":3,"name":"action with longer name","storiesURL":"/stories/"}],
              "results": [{"id":1,"name":"r1","storiesURL":"/stories/"},{"id":2,"name":"r2","storiesURL":"/stories/"},{"id":3,"name":"r3","storiesURL":"/stories/"},{"id":4,"name":"r4","storiesURL":"/stories/"}],
              "a2r": [{"from":1,"to":1,"storiesURL":"/stories/"},{"from":1,"to":1,"storiesURL":"/stories/"},{"from":2,"to":2,"storiesURL":"/stories/"},{"from":2,"to":3,"storiesURL":"/stories/"},{"from":3,"to":4,"storiesURL":"/stories/"}],
              "r2g": [{"from":1,"storiesURL":"/stories/"},{"from":2,"storiesURL":"/stories/"},{"from":3,"storiesURL":"/stories/"},{"from":4,"storiesURL":"/stories/"}]  }""" % (g.id, g.name, g.short_description, g.id)
    return HttpResponse(res)

def stories(request,goal_id):
    g = get_object_or_404(Goal, pk=goal_id)
    return HttpResponse("stories not implemented yet :S")
