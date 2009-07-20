from ecclesia.goals.models import *
from ecclesia.operations.models import *

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse


def visualize(request,goal_id):
    context = dict()
    return render_to_response('visualize_canvas.html', {'context':context})

def json(request,goal_id):
    return """
    
"""