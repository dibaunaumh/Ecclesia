# This Python file uses the following encoding: utf-8
from ecclesia.goals.models import *
from ecclesia.operations.models import *
from ecclesia.discussion.forms import get_story_form_for_object

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.http import HttpResponse


def visualize(request,goal_id):
    goal = get_object_or_404(Goal, pk=goal_id)
    group = goal.group_profile
    return render_to_response('visualize_canvas.html', locals())

def get_path_resolution_data(request,goal_id):
    """
    Returns the data for the Goal path resolution page.
    Hack alert: JSON rendering logic is included in the view. Todo: remove JSON rendering, which should remain exclusively in the template.
    """
    goal = get_object_or_404(Goal, pk=goal_id)
    actions = CourseOfAction.objects.filter(goal=goal)
    actions_list = ",".join(['{"id":%d,"name":"%s","storiesURL":"/stories/"}' % (action.id, action.name) for action in actions]) 
    results = PossibleResult.objects.filter(goal=goal)
    results_list = ",".join(['{"id":%d,"name":"%s","storiesURL":"/stories/"}' % (result.id, result.name) for result in results]) 
    causing_relations = []
    for action in actions:
        for cr in CausingRelation.objects.filter(course_of_action=action):
            causing_relations.append(cr)
    causing_relations_list = ",".join(['{"from":%d,"to":%d,"storiesURL":"/stories/"}' % (cr.course_of_action.id, cr.possible_result.id) for cr in causing_relations])
    leading_relations = []
    for result in results:
        for lr in LeadingRelation.objects.filter(possible_result=result):
            leading_relations.append(lr)
    leading_relations_list = ",".join(['{"from":%d,"storiesURL":"/stories/"}' % lr.possible_result.id for lr in leading_relations])
    return render_to_response('path_resolution_data.json', locals())


def get_number_of_stories(request,goal_id):
    g = get_object_or_404(Goal, pk=goal_id)
    num_stories = g.stories.count()
    return HttpResponse('%d' % num_stories)


def stories(request,goal_id):
    g = get_object_or_404(Goal, pk=goal_id)
    stories = g.stories.all()
    return render_to_response('goal_stories_miniform.html', locals())

def write_story(request, goal_id):
    g = get_object_or_404(Goal, pk=goal_id)
    form = get_story_form_for_object(g)
    return render_to_response('write_story_miniform.html', {'form':form})
    

def create_possible_result(request,goal_id):
# return a form used to create possible result
    g = get_object_or_404(Goal, pk=goal_id)
    return HttpResponse("create possible result not implemented yet :S")

def create_course_of_action(request,goal_id):
# return a form used to create course of action
    g = get_object_or_404(Goal, pk=goal_id)
    return HttpResponse("create course of action not implemented yet :S")
