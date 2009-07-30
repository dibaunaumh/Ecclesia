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
    res = u"""{"goal": {"id": %d, "name": "%s","short_description": "%s"},     
              "actions": [{"id":1,"name":"a1"},{"id":2,"name":"action2"},{"id":3,"name":"action with longer name"}],
              "results": [{"id":1,"name":"r1"},{"id":2,"name":"r2"},{"id":3,"name":"r3"},{"id":4,"name":"r4"}],
              "a2r": [{"from":1,"to":1},{"from":1,"to":1},{"from":2,"to":2},{"from":2,"to":3},{"from":3,"to":4}],
              "r2g": [{"from":1},{"from":2},{"from":3},{"from":4}]  }""" % (g.id, g.name, g.short_description)
    return HttpResponse(res)