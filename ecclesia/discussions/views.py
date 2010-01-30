from django.contrib.auth.models import Group, User
from ecclesia.discussions.models import Story, Discussion
from ecclesia.groups.models import GroupProfile, GroupPermission
from ecclesia.discussions.forms import StoryForm
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django import forms
from forms import *
from services.search_filter_pagination import search_filter_paginate

def visualize(request, discussion_slug):
    discussion = Discussion.objects.get(slug=discussion_slug)
    group = GroupProfile.objects.get(group=Group.objects.get(id=discussion.group.pk))
    stories = Story.objects.filter(discussion=discussion.pk)
    user_in_group = False
    try:
        user_in_group = request.user.groups.filter(id=group.group.id).count() > 0
    except:
        pass
    #initializing the form
    show_errors_in_form = False
    story_form = StoryForm()
    #saving new story
    if request.POST:
        story_form = StoryForm(request.POST)
        if story_form.is_valid():
            story = Story()
            story.discussion = discussion
            story.name = story_form.cleaned_data['name']
            story.slug = story_form.cleaned_data['slug']
            story.content = story_form.cleaned_data['content']
            story.speech_act = story_form.cleaned_data['speech_act']
            story.created_by = request.user
            story.save()
            story_form = StoryForm()
        else:
            show_errors_in_form = True
    #adding beautiful css
    for key in story_form.fields:
        story_form.fields[key].widget.attrs["class"] = "text ui-widget-content ui-corner-all"
    return render_to_response('discussion_home.html', locals())

#def submit_story(request):
#    story = Story(created_by=request.user)
#    form = StoryForm(request.POST, instance=story)
#    try:
#        form.save()
#    except ValueError:
#        return render_to_response('write_story_miniform.html', {'form':form})
#    return HttpResponse('OK')

def discussions_list(request, group_slug):
    group = GroupProfile.objects.filter(slug=group_slug)
    if group.count() == 0:
        raise Http404("Can't find a group with the slug: %s" % group_slug)
    else:
        user=request.user
        if str(user) != 'AnonymousUser':
            if GroupPermission.objects.filter(group=group[0]).filter(user=user):
                permission = GroupPermission.objects.filter(group=group[0]).filter(user=user)[0]
                user_permission_type = permission.permission_type
    discussions = Discussion.objects.filter(group=group[0])
    (my_items, get_parameters, f) = search_filter_paginate('discussion', discussions, request)
    return render_to_response('discussions_list.html', locals())

def delete_discussion(request, discussion_pk):
    discussion = Discussion.objects.get(pk=discussion_pk)
    group = discussion.group
    discussion.delete()
    return HttpResponseRedirect('/discussions_list/%s/' % group.slug)

def stories_list(request, discussion_slug):
    discussion = Discussion.objects.filter(slug=discussion_slug)
    if discussion.count() == 0:
        raise Http404("Can't find a discussion with the slug: %s" % discussion_slug)
    else:
        user=request.user
        if str(user) != 'AnonymousUser':
            if GroupPermission.objects.filter(group=discussion[0].group).filter(user=user):
                permission = GroupPermission.objects.filter(group=discussion[0].group).filter(user=user)[0]
                user_permission_type = permission.permission_type
    stories = Story.objects.filter(discussion=discussion[0])
    (my_items, get_parameters, f) = search_filter_paginate('story', stories, request)
    return render_to_response('stories_list.html', locals())

def delete_story(request, story_pk):
    story = Story.objects.get(pk=story_pk)
    discussion = story.discussion
    story.delete()
    return HttpResponseRedirect('/stories_list/%s/' % discussion.slug)