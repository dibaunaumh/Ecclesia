from ecclesia.groups.models import GroupProfile, GroupPermission, MissionStatement
from ecclesia.discussions.forms import StoryForm
from ecclesia.discussions.models import *
from ecclesia.notifications.models import Notification
from django.contrib.auth.models import Group, User
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django import forms
from forms import *
from services.search_filter_pagination import search_filter_paginate
from django.core import serializers
from django.template.defaultfilters import slugify
import datetime
import discussion_actions

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
    speech_acts = SpeechAct.objects.filter(discussion_type=discussion.type)
    opinion_types = speech_acts.filter(story_type=2)
    last_related_update = str(discussion.last_related_update) # set an initial value for the update timestamp
    return render_to_response('discussion_home.html', locals())

def evaluate(request, discussion_slug):
    discussion = get_object_or_404(Discussion, slug=discussion_slug)
    conclusions = discussion_actions.evaluate_stories(discussion)
    json = serializers.serialize('json', conclusions, ensure_ascii=False)
    return HttpResponse(json)

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

def add_discussion(request):
    if request.POST:
        discussion_form = DiscussionForm(request.POST)
        if discussion_form.is_valid():
            discussion = Discussion()
            discussion.group = Group.objects.get(id=request.POST.get('group'))
            discussion.type = DiscussionType.objects.get(id=request.POST.get('type'))
            discussion.name = discussion_form.cleaned_data['name']
            discussion.slug = slugify(discussion_form.cleaned_data['name'])
            discussion.description = discussion_form.cleaned_data['description']
            discussion.created_by = request.user
            discussion.x = request.POST.get('x', None)
            discussion.y = request.POST.get('y', None)
            discussion.save()
            return HttpResponse('reload')
        else:
            return HttpResponse('error')
    else:
        return HttpResponse('Wrong usage: HTTP POST expected')

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
#    x = request.POST.get('x', None)
    y = request.POST.get('y', None)
    story = Story()
    story.discussion = discussion
    story.created_by = user
    story.title = title
    story.slug = slug
    story.speech_act = speech_act
#    if x:
#        story.x = x
    if y:
        story.y = y
    story.save()
    notification = Notification(text="There is a new story in %s discussion: %s" % (discussion.slug, title), 
                 group=discussion.group)
    #notification.save()
    return HttpResponse("reload")

def add_opinion(request, discussion, user, title, slug, speech_act):
    parent_story = request.POST.get('parent_story', None)
    parent_class = request.POST.get('parent_class', None)
    if parent_story is None:
        return HttpResponse("Did not get parent story.")
    if parent_class is None:
        return HttpResponse("Did not get parent type.")
    opinion = Opinion()
    opinion.discussion = discussion
    opinion.created_by = user
    opinion.title = title
    opinion.slug = slug
    opinion.speech_act = speech_act
    opinion.parent_story = {
        '1': Story.objects.get,
        '2': Opinion.objects.get,
        '3': StoryRelation.objects.get
    }[parent_class](pk=parent_story)
    opinion.save()
    notification = Notification(text="There is a new opinion in %s discussion: %s" % (discussion.slug, title), 
                 group=discussion.group)
    #notification.save()
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
    conclusions = DiscussionConclusion.objects.filter(discussion=discussion)
    conclusions_map = {}
    for c in conclusions:
        conclusions_map[c.story.id] = True
    json = ','
    for story in stories:
        is_conclusion = "true" if story.id in conclusions_map else "false"
        children = story.get_children_js_array()
        json = '%s{"story":{"id":%s,"url":"%s","name":"%s","type":"%s","content":"%s","state":{"indicated":%s},"dimensions":{"x":%s,"y":%s,"w":%s,"h":%s},"children":%s}},' % (json, story.id, story.get_absolute_url(), story.title, story.speech_act, story.content, is_conclusion, story.x, story.y, story.w, story.h, children)
    relations = StoryRelation.objects.filter(discussion=discussion)
    for relation in relations:
        children = relation.get_children_js_array()
        json = '%s{"relation":{"id":%s,"url":"%s","name":"%s","type":"%s","from_id":"%s","to_id":"%s","children":%s}},' % (json, relation.id, relation.get_absolute_url(), relation.title, relation.speech_act, relation.from_story.unique_id(), relation.to_story.unique_id(), children)
    opinions = Opinion.objects.filter(discussion=discussion)
    for opinion in opinions:
        json = '%s{"opinion":{"id":%s,"url":"%s","name":"%s","type":"%s","parent_id":"%s"}},' % (json, opinion.id, opinion.get_absolute_url(), opinion.title, opinion.speech_act, opinion.parent_story.unique_id())
    #json_serializer = serializers.get_serializer("json")()
    #json_serializer.serialize(groups, ensure_ascii=False, stream=response, fields=('x', 'y', 'w', 'h'))
    json = json.strip(',')
    return HttpResponse('[%s]' % json)

def get_visualization_meta_data(request):
    discussion_type = request.GET.get('discussion_type', 1)
    speech_acts = SpeechAct.objects.filter(discussion_type=discussion_type).order_by('story_type','ordinal')
    json = serializers.serialize('json', speech_acts, ensure_ascii=False)
    return HttpResponse(json)

def status(request, discussion_slug):
    datetime_format = '%Y-%m-%d %H:%M:%S.%f'
    discussion = Discussion.objects.get(slug=discussion_slug)
    last_changed_db = discussion.last_related_update
    last_changed_client = request.POST.get('last_changed', None)
    if not last_changed_client:
        return HttpResponse(str(last_changed_db))
    else:
        try:
            last_changed_client = datetime.datetime.strptime(last_changed_client, datetime_format)
            if last_changed_client < last_changed_db:
                last_changed_client = last_changed_db
            return HttpResponse(str(last_changed_client))
        except: # probably the last_changed value isn't in the right format
            return HttpResponse(str(last_changed_db))

def discussions_list(request, group_slug):
    group = GroupProfile.objects.filter(slug=group_slug)
    if group.count() == 0:
        raise Http404("Can't find a group with the slug: %s" % group_slug)
    else:
        group = group[0]
        user=request.user
        if str(user) != 'AnonymousUser':
            if GroupPermission.objects.filter(group=group).filter(user=user):
                permission = GroupPermission.objects.filter(group=group).filter(user=user)[0]
                user_permission_type = permission.permission_type
    discussions = Discussion.objects.filter(group=group)
    (my_items, get_parameters, f) = search_filter_paginate('discussion', discussions, request)
    return render_to_response('discussions_list.html', locals())

def delete_discussion(request, discussion_pk):
    discussion = Discussion.objects.get(pk=discussion_pk)
    group = discussion.group
    discussion.delete()
    return HttpResponseRedirect('/discussions_list/%s/' % group.slug)

def stories_list(request, discussion_slug):
    discussion = Discussion.objects.filter(slug=discussion_slug)
    group = discussion[0].group
    if discussion.count() == 0:
        raise Http404("Can't find a discussion with the slug: %s" % discussion_slug)
    else:
        discussion = discussion[0]
        group = discussion.group
        user=request.user
        if str(user) != 'AnonymousUser':
            if GroupPermission.objects.filter(group=discussion.group).filter(user=user):
                permission = GroupPermission.objects.filter(group=discussion.group).filter(user=user)[0]
                user_permission_type = permission.permission_type
        user_in_group = check_if_user_in_group(user, discussion)
    stories = Story.objects.filter(discussion=discussion)
    (my_items, get_parameters, f) = search_filter_paginate('story', stories, request)
    return render_to_response('stories_list.html', locals())

def delete_story(request, story_pk):
    story = Story.objects.get(pk=story_pk)
    discussion = story.discussion
    story.delete()
    return HttpResponseRedirect('/stories_list/%s/' % discussion.slug)

def delete_relation(request, relation_pk):
    response = ''
    if relation_pk:
        relation = StoryRelation.objects.get(pk=relation_pk)
        relation.delete()
        response = 'reload'
    return HttpResponse(response)

def get_inline_field(request):
    fieldname = request.POST['id']
    if fieldname.split("_")[0] == 'discussion':
        discussion = Discussion.objects.get(pk=fieldname.split("_")[1])
        discussion.name = request.POST['value']
        discussion.save()
        return HttpResponse("%s" % discussion.name)
    if fieldname.split("_")[0] == 'storytitle':
        story = Story.objects.get(pk=fieldname.split("_")[1])
        story.title = request.POST['value']
        story.slug = slugify(story.title)
        story.save()
        return HttpResponse("%s" % story.title)
    if fieldname.split("_")[0] == 'storycontent' or fieldname.split("_")[0] == 'storycontent2':
        story = Story.objects.get(pk=fieldname.split("_")[1])
        story.content = request.POST['value']
        story.save()
        return HttpResponse("%s" % story.content)
    if fieldname.split("_")[0] == 'missionstatement':
        mission_statement = MissionStatement.objects.get(pk=fieldname.split("_")[1])
        mission_statement.mission_statement = request.POST['value']
        mission_statement.save()
        return HttpResponse("%s" % mission_statement.mission_statement)

def check_if_user_in_group(user, discussion):
    user_in_group = False
    try:
        user_in_group = user.groups.filter(id=discussion.group.id).count() > 0
    except:
        pass
    return user_in_group

def story_home(request, discussion_slug, ctype, slug):
    discussion = Discussion.objects.get(slug=discussion_slug)
    object = {
        'story'     : Story.objects.get,
        'relation'  : StoryRelation.objects.get
    }[ctype](slug=slug, discussion=discussion)

    group = GroupProfile.objects.get(group=Group.objects.get(id=discussion.group.pk))
    user = request.user
    opinions = object.opinions.all().order_by('speech_act')
    user_in_group = check_if_user_in_group(user, discussion)
    return render_to_response('story_home.html', locals())

def merge_stories(story1_slug, story2_slug):
    story1 = get_object_or_404(Story, slug=story1_slug)
    story2 = get_object_or_404(Story, slug=story2_slug)
    if not story1.parent: #story1 is not a group
        story1.parent = story2
        story2.is_parent = True
        #change_from_relation(story1, story2)
    else:
        if not story2.parent: #story1 - group, story2 - not
            story2.parent = story1.parent
            #change_from_relation(story2, story1)
        else: #both stories are group stories
            for story in Story.objects.filter(parent=story1):
                story.parent = story2
                story.save()
                #change_from_relation(story, story2)
            story1.parent = story2
            story1.is_parent = False
            #change_from_relation(story1, story2)
    story1.save()
    story2.save()
   
def extract_stories(story1, story2_slug):
    #how to return merged relations?
    pass
 
def change_from_relation(story1, story2):
    for relation in StoryRelation.objects.filter(from_story=story1):
        relation.from_story=story2
        relation.save()