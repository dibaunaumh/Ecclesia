from ecclesia.groups.models import GroupProfile, GroupPermission, MissionStatement
from ecclesia.discussions.forms import StoryForm
from ecclesia.discussions.models import *
from django.contrib.auth.models import Group, User
from django.shortcuts import render_to_response,get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django import forms
from forms import *
from services.search_filter_pagination import search_filter_paginate
from django.core import serializers
from django.template.defaultfilters import slugify

def visualize(request, discussion_slug):
    user=request.user
    discussion = Discussion.objects.get(slug=discussion_slug)
    group = GroupProfile.objects.get(group=Group.objects.get(id=discussion.group.pk))
    stories = Story.objects.filter(discussion=discussion.pk)
    user_in_group = False
    try:
        user_in_group = user.groups.filter(id=group.group.id).count() > 0
    except:
        pass
    #initializing the form
    show_errors_in_form = False
    story_form = StoryForm()
    #saving new story
    if request.POST:
        story_form = StoryForm(request.POST)
        if story_form.is_valid():
            save_story_from_form(story_form, discussion, user)
            story_form = StoryForm()
        else:
            show_errors_in_form = True
    #adding beautiful css
    for key in story_form.fields:
        story_form.fields[key].widget.attrs["class"] = "text ui-widget-content ui-corner-all"
    speech_acts = SpeechAct.objects.filter(story_type=1) # 'story' as default
    return render_to_response('discussion_home.html', locals())


def get_stories_json(request):
    """
    Used by an AJAX call from the story adding GUI.
    """
    result = HttpResponse('[]')
    if request.GET:
        discussion_slug = request.GET.get('discussion_slug', None)
        if discussion_slug is None:
            return result
        discussion = Discussion.objects.get(slug=discussion_slug)
        stories = Story.objects.filter(discussion=discussion.pk)
        json = serializers.serialize('json', stories, ensure_ascii=False)
        result = HttpResponse(json)
    return result


def add_base_story(request):
    #saving new story
    if request.POST:
        discussion = get_object_or_404(Discussion, pk=request.POST["discussion"])
        story_type = request.POST["story-class"]
        title = request.POST["title"]
        slug = slugify(title)
        user = request.user
        speech_act = get_object_or_404(SpeechAct, pk=int(request.POST["speech_act"]))
        result = {
            '1': add_story,
            '2': add_opinion,
            '3': add_relation,
        }[story_type](request, discussion, user, title, slug, speech_act)
    else:
        result = HttpResponse("Wrong usage: HTTP POST expected")
    return result


def add_story(request, discussion, user, title, slug, speech_act):
    story = Story()
    story.discussion = discussion
    story.created_by = user
    story.title = title
    story.slug = slug
    story.speech_act = speech_act
    story.save()
    return HttpResponse("reload")

def add_opinion(request, discussion, user, title, slug, speech_act):
    parent_story = request.POST.get('parent_story', None)
    if parent_story is None:
        return HttpResponse("Did not get parent story.")
    opinion = Opinion()
    opinion.discussion = discussion
    opinion.created_by = user
    opinion.title = title
    opinion.slug = slug
    opinion.speech_act = speech_act
    opinion.parent_story = Story.objects.get(pk=parent_story)
    opinion.save()
    return HttpResponse("reload")

def add_relation(request, discussion, user, title, slug, speech_act):
    from_story = request.POST.get('from_story', None)
    to_story = request.POST.get('to_story', None)
    if from_story is None or to_story is None:
        return HttpResponse("Did not get from and to stories.")
    relation = StoryRelation()
    relation.discussion = discussion
    relation.created_by = user
    relation.title = title
    relation.slug = slug
    relation.speech_act = speech_act
    relation.from_story = Story.objects.get(pk=from_story)
    relation.to_story = Story.objects.get(pk=to_story)
    relation.save()
    return HttpResponse("reload")


def get_stories_view_json(request, discussion_slug):
    discussion = Discussion.objects.get(slug=discussion_slug)
    stories = Story.objects.filter(discussion=discussion)
    json = ','
    for story in stories:
        json = '%s{"story":{"id":%s,"url":"%s","name":"%s","type":"%s","dimensions":{"x":%s,"y":%s,"w":%s,"h":%s}}},' % (json, story.id, story.get_absolute_url(), story.title, story.speech_act, story.x, story.y, story.w, story.h)
    relations = StoryRelation.objects.filter(discussion=discussion)
    for relation in relations:
        json = '%s{"relation":{"id":%s,"url":"%s","name":"%s","type":"%s","from_id":"%s","to_id":"%s"}},' % (json, relation.id, relation.get_absolute_url(), relation.title, relation.speech_act, relation.from_story.unique_id(), relation.to_story.unique_id())
    opinions = Opinion.objects.filter(discussion=discussion)
    for opinion in opinions:
        json = '%s{"opinion":{"id":%s,"url":"%s","name":"%s","type":"%s","parent_id":"%s"}},' % (json, opinion.id, opinion.get_absolute_url(), opinion.title, opinion.speech_act, opinion.parent_story.unique_id())
    #json_serializer = serializers.get_serializer("json")()
    #json_serializer.serialize(groups, ensure_ascii=False, stream=response, fields=('x', 'y', 'w', 'h'))
    json = json.strip(',')
    return HttpResponse('[%s]' % json)

def get_visualization_meta_data(request):
    speech_acts = SpeechAct.objects.order_by('story_type','ordinal')
    json = serializers.serialize('json', speech_acts, ensure_ascii=False)
    return HttpResponse(json)

def get_speech_acts_by_story_type(request):
    story_type = request.GET.get('story_type', 1)
    speech_acts = SpeechAct.objects.filter(story_type=story_type)
    json = serializers.serialize('json', speech_acts, ensure_ascii=False)
    return HttpResponse(json)

def save_story_from_form(story_form, discussion, user):
    story = Story()
    story.discussion = discussion
    story.title = story_form.cleaned_data['title']
    story.slug = story_form.cleaned_data['slug']
    story.content = story_form.cleaned_data['content']
    story.speech_act = story_form.cleaned_data['speech_act']
    story.created_by = user
    story.save()
    return

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
        user_in_group = False
        try:
            user_in_group = user.groups.filter(id=discussion[0].group.id).count() > 0
        except:
            pass
    stories = Story.objects.filter(discussion=discussion[0])
    (my_items, get_parameters, f) = search_filter_paginate('story', stories, request)
    return render_to_response('stories_list.html', locals())

def delete_story(request, story_pk):
    story = Story.objects.get(pk=story_pk)
    discussion = story.discussion
    story.delete()
    return HttpResponseRedirect('/stories_list/%s/' % discussion.slug)

def get_inline_field(request):
    fieldname = request.POST['id']
    if fieldname.split("_")[0] == 'discussion':
        discussion = Discussion.objects.get(pk=fieldname.split("_")[1])
        discussion.name = request.POST['value']
        discussion.save()
        return HttpResponse("%s" % discussion.name)
    if fieldname.split("_")[0] == 'story':
        story = Story.objects.get(pk=fieldname.split("_")[1])
        story.content = request.POST['value']
        story.save()
        return HttpResponse("%s" % story.content)
    if fieldname.split("_")[0] == 'missionstatement':
        mission_statement = MissionStatement.objects.get(pk=fieldname.split("_")[1])
        mission_statement.mission_statement = request.POST['value']
        mission_statement.save()
        return HttpResponse("%s" % mission_statement.mission_statement)