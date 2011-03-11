import sys
from django.contrib.auth.models import Group

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseServerError
from django.core import serializers
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.contrib import messages
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.utils import simplejson
from django.conf import settings
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt
from discussions.models import Discussion, DiscussionType, DiscussionType
from discussions.workflow_hints import get_workflow_hints

from forms import *
import discussion_actions
from ecclesia.groups.models import GroupPermission, MissionStatement
from ecclesia.discussions.models import *
from notifications.services import create_notification
from ecclesia.common.views import _follow, _unfollow
from ecclesia.common.utils import is_heb
from ecclesia.common.decorators import *
from groups.models import GroupProfile, UserProfile
from services.search_filter_pagination import search_filter_paginate
from services.utils import get_user_permissions
from ecclesia.voting.models import Voting
from ecclesia.voting.services import get_voting_data
from coa_workflow_manager import *

DEFAULT_FORM_ERROR_MSG = 'Your input was invalid. Please correct and try again.'
UNIQUENESS_ERROR_PATTERN = 'already exists'

#@notify_not_logged_in
def visualize(request, discussion_slug):
    user = request.user
    discussion = Discussion.objects.select_related(depth=1).get(slug=discussion_slug)
    group = GroupProfile.objects.get(group=discussion.group)
    stories = discussion.stories
    user_in_group = group.is_user_in_group(request.user)
    voting = Voting.objects.get_started(discussion=discussion)
    if voting:
        has_voting = True
        voting_data = get_voting_data(user, voting, discussion)
        if voting_data is False:
            has_voting = False
    if discussion.is_private and not group.is_user_in_group(user):
        messages.error(request, "The discussion is private. You're not allowed to see it." )
    if str(user) != 'AnonymousUser':
        user_follows_discussion = True if user.subscriptions.filter(discussion=discussion) else False
    else:
        user_follows_discussion = False
    speech_acts = SpeechAct.objects.filter(discussion_type=discussion.type)
    opinion_types = speech_acts.filter(story_type=2)
    last_related_update = str(discussion.last_related_update) # set an initial value for the update timestamp
    user_permissions = get_user_permissions(request.user, group)
    if user_permissions != 3 and user_permissions != "Not logged in":
        user_permissions = 'allowed'
    else:
        user_permissions = ''
    hints_metadata = get_hints_metadata(discussion)
    return render_to_response('discussion_home.html', locals(), context_instance=RequestContext(request))

def get_update(request, discussion_slug):
    discussion = get_object_or_404(Discussion, slug=discussion_slug)
    group = GroupProfile.objects.get(group=discussion.group)
    user_in_group = group.is_user_in_group(request.user)

    if user_in_group:
        workflow_status = discussion.workflow_status
    else:
        workflow_status = NOT_ALLOWED_TO_EDIT

    results = []
    discussion = get_object_or_404(Discussion, slug=discussion_slug)
    results.append('"elements":%s' % get_stories_view_json(request, discussion))
    results.append('"workflow_status":%s' % workflow_status)
    json = '{"discussion":{%s}}' % ','.join(results)
    return HttpResponse(json)

def evaluate(request, discussion_slug):
    discussion = get_object_or_404(Discussion, slug=discussion_slug)
    conclusions = discussion_actions.evaluate_stories_verbose(discussion)
    json = simplejson.dumps(conclusions)
    return HttpResponse(json)

def add_discussion(request):
    group = Group.objects.get(id=request.POST.get('group'))
    group_profile = GroupProfile.objects.filter(group=group)[0]
    if group_profile.is_private and not group_profile.is_user_in_group(request.user):
        return HttpResponse("The group is private. You're not allowed to create discussion.")
    if request.POST:
        discussion_form = DiscussionForm(request.POST)
        if discussion_form.is_valid():
            discussion = Discussion()
            discussion.group = group
            discussion.type = DiscussionType.objects.get(id=request.POST.get('type'))
            discussion.name = discussion_form.cleaned_data['name']
            if is_heb(discussion.name):
                encoded_discussion_name = discussion.name.__repr__().encode("ascii")[2:-1]
                encoded_group_name = group.name.__repr__().encode("ascii")[2:-1]
                discussion.slug = slugify("%s_%s" % (encoded_group_name,encoded_discussion_name))
            else:
                discussion.slug = slugify("%s_%s" % (group.name,discussion.name))
            discussion.description = discussion_form.cleaned_data['description']
            discussion.created_by = request.user
            discussion.x = request.POST.get('x', None)
            discussion.y = request.POST.get('y', None)
            discussion.is_private = 'is_private' in request.POST
            discussion.save()
            return HttpResponse('reload')
        else:
            return HttpResponse(discussion_form.errors.as_text(), status=400)
    else:
        return HttpResponse('Wrong usage: HTTP POST expected')

@csrf_exempt
def create_discussion_via_im(request):
    im_address = request.POST.get("im_address", "")
    name = request.POST.get("name", _("Untitled"))
    description = request.POST.get("description", "")
    group = int(request.POST.get("group", 0))
    user_profile = get_object_or_404(UserProfile, im_address=im_address)
    user = user_profile.user
    group = get_object_or_404(Group, pk=group)
    discussion = Discussion()
    discussion.group = group
    discussion.type = DiscussionType.objects.get(name=settings.DEFAULT_DISCUSSION_TYPE)
    discussion.name = name
    if is_heb(discussion.name):
        encoded_discussion_name = discussion.name.__repr__().encode("ascii")[2:-1]
        encoded_group_name = group.name.__repr__().encode("ascii")[2:-1]
        discussion.slug = slugify("%s_%s" % (encoded_group_name,encoded_discussion_name))
    else:
        discussion.slug = slugify("%s_%s" % (group.name,discussion.name))
    discussion.description = description
    discussion.created_by = user
    discussion.x = 0
    discussion.y = 0
    discussion.is_private = 'is_private' in request.POST
    discussion.save()
    discussion_details = {"id": discussion.id, "link": discussion.get_absolute_url(), "name": discussion.name}
    return HttpResponse(simplejson.dumps(discussion_details))

def add_base_story(request):
    #saving new story
    if request.POST:
        discussion = get_object_or_404(Discussion, pk=request.POST["discussion"])
        story_type = request.POST["story-class"]
        title = request.POST["title"]
        if is_heb(title):
            encoded_title = title.__repr__().encode("ascii")[2:-1]
            slug = slugify(encoded_title)
        else:
            slug = slugify(title)
        user = request.user
        speech_act = get_object_or_404(SpeechAct, pk=int(request.POST["speech_act"]))
        result = {
            '1': add_story,
            '2': add_opinion,
            '3': add_relation,
        }[story_type](request, discussion, user, title, slug, speech_act)
    else:
        result = HttpResponse(_("Wrong usage: HTTP POST expected"))
    return result

def add_story(request, discussion, user, title, slug, speech_act):
#    x = request.POST.get('x', None)
    y = request.POST.get('y', None)
    group_profile = GroupProfile.objects.filter(group=discussion.group)[0]
    if discussion.is_private and not group_profile.is_user_in_group(request.user):
        return HttpResponse("The discussion is private. You're not allowed to create story.")
    try:
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
        try:
            story.full_clean()
        except ValidationError, e:
            message = DEFAULT_FORM_ERROR_MSG
            if e.message_dict[NON_FIELD_ERRORS] and re.search(UNIQUENESS_ERROR_PATTERN, e.message_dict[NON_FIELD_ERRORS][0]):
                message = _('Oops! A story with this title was already created inside this discussion.')
            resp = HttpResponse(message)
            resp.status_code = 500
            return resp

        story.save()
        resp = HttpResponse("%s" % discussion.last_related_update)

        create_notification(text="There is a new story in %s discussion: %s" % (discussion.slug, title),
                                        entity=story, acting_user=request.user)
    except:
        resp = HttpResponse(str(sys.exc_info()[1]))
        resp.status_code = 500

    return resp

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
    try:
        try:
            opinion.full_clean()
        except ValidationError, e:
            message = DEFAULT_FORM_ERROR_MSG
            if e.message_dict[NON_FIELD_ERRORS] and re.search(UNIQUENESS_ERROR_PATTERN, e.message_dict[NON_FIELD_ERRORS][0]):
                message = _('Oops! An opinion with this title was already created inside this discussion.')
            resp = HttpResponse(message)
            resp.status_code = 500
            return resp

        opinion.save()
        resp = HttpResponse("%s" % discussion.last_related_update)

        create_notification(text="There is a new opinion in %s discussion: %s" % (discussion.slug, title),
                     entity=opinion, acting_user=request.user)
    except:
        resp = HttpResponse(str(sys.exc_info()[1]))
        resp.status_code = 500

    return resp

def add_relation(request, discussion, user, title, slug, speech_act):
    from_story = request.POST.get('from_story', None)
    to_story = request.POST.get('to_story', None)
    if from_story is None or to_story is None:
        resp = HttpResponse(_("Did not get from and to stories."))
        resp.status_code = 500
        return resp
    relation = StoryRelation()
    relation.discussion = discussion
    relation.created_by = user
    relation.title = title
    relation.slug = slug
    relation.speech_act = speech_act
    relation.from_story = Story.objects.get(pk=from_story)
    relation.to_story = Story.objects.get(pk=to_story)
    try:
        try:
            relation.full_clean()
        except ValidationError, e:
            message = DEFAULT_FORM_ERROR_MSG
            if e.message_dict[NON_FIELD_ERRORS] and re.search(UNIQUENESS_ERROR_PATTERN, e.message_dict[NON_FIELD_ERRORS][0]):
                message = _('Oops! A relation with this title was already created inside this discussion.')
            resp = HttpResponse(message)
            resp.status_code = 500
            return resp

        relation.save()
        resp = HttpResponse("%s" % discussion.last_related_update)

        create_notification(text="There is a new relation in %s discussion: %s" % (discussion.slug, title),
                                        entity=relation, acting_user=request.user)
    except:
       resp = HttpResponse(str(sys.exc_info()[1]))
       resp.status_code = 500

    return resp

def get_stories_view_json(request, discussion):
    voting = Voting.objects.get_started(discussion=discussion)
    stories = discussion.stories.all()
    conclusions = discussion.discussionconclusion_set.all()
    conclusions_map = {}
    for c in conclusions:
        conclusions_map[c.story.id] = True
    decisions_map = {}
    decisions = discussion.decisions.all()
    for decision in decisions:
        decisions_map[decision.decision_story.id] = True
    json = ','
    for story in stories:
        is_conclusion = "true" if story.id in conclusions_map else "false"
        is_decision = "true" if story.id in decisions_map else "false"
        children = story.get_children_js_array()
        ballots = 0
        if voting:
            ballots = 0 if not story.ballots else story.ballots.filter(user=request.user,voting=voting).count()
        icon = ''
        if story.speech_act.icon:
            icon = '%s%s' % (settings.MEDIA_URL, story.speech_act.icon)
        json = '%s{"story":{"id":%s,"url":"%s","name":"%s","type":"%s","content":"%s","ballots":%s,"state":{"indicated":%s,"decided":%s},"dimensions":{"x":%s,"y":%s,"w":%s,"h":%s},"children":%s,"icon":"%s"}},' % (json, story.id, story.get_absolute_url(), story.get_json_safe_title(), story.speech_act, story.get_json_safe_content(), ballots, is_conclusion, is_decision, story.x, story.y, story.w, story.h, children, icon)
    relations = discussion.relations.all()
    for relation in relations:
        children = relation.get_children_js_array()
        json = '%s{"relation":{"id":%s,"url":"%s","name":"%s","type":"%s","from_id":"%s","to_id":"%s","children":%s}},' % (json, relation.id, relation.get_absolute_url(), relation.get_json_safe_title(), relation.speech_act, relation.from_story.unique_id(), relation.to_story.unique_id(), children)
    opinions = discussion.opinions.all()
    for opinion in opinions:
        json = '%s{"opinion":{"id":%s,"url":"%s","name":"%s","type":"%s","parent_id":"%s"}},' % (json, opinion.id, opinion.get_absolute_url(), opinion.get_json_safe_title(), opinion.speech_act, opinion.parent_story.unique_id())
    #json_serializer = serializers.get_serializer("json")()
    #json_serializer.serialize(groups, ensure_ascii=False, stream=response, fields=('x', 'y', 'w', 'h'))
    json = json.strip(',')
#    return HttpResponse('[%s]' % json)
    return '[%s]' % json

def get_visualization_meta_data(request):
    discussion_type = request.GET.get('discussion_type', 1)
    speech_acts = SpeechAct.objects.filter(discussion_type=discussion_type).order_by('story_type','ordinal')
    json = serializers.serialize('json', speech_acts, ensure_ascii=False)
    return HttpResponse(json)

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
    discussions = Discussion.objects.filter(group=group.group)
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

def edit_opinion(request):
    result = ''
    if request.POST:
        pk = request.POST.get('pk', None)
        if not pk:
            result = '[{"error":"Missing opinion\'s ID."}]'
        else:
            opinion = Opinion.objects.get(pk=pk)
            title = request.POST.get('title', None)
            if title:
                opinion.title = title
                opinion.slug = slugify(title)
            opinion.content = request.POST.get('content', '')
            speech_act = request.POST.get('speech_act', None)
            if speech_act:
                speech_act = SpeechAct.objects.get(pk=speech_act)
                opinion.speech_act = speech_act
            opinion.save()
#            result = serializers.serialize('json', (opinion,), ensure_ascii=False)
            result = '[{"pk":%d, "fields":{"speech_act":"%s","title":"%s","content":"%s"}}]' % (opinion.pk, opinion.speech_act, opinion.get_json_safe_title(), opinion.get_json_safe_content())
    else:
        result = "Wrong usage: HTTP POST expected"
    return HttpResponse(result)

def delete_story(request):
    if request.POST:
        story_pk = request.POST.get('story', None)
        if story_pk:
            try:
                story = Story.objects.get(pk=story_pk)
                story.delete()
                return HttpResponse('OK')
            except:
                return HttpResponseServerError(_('Could not find requested story.'))
        return HttpResponseServerError(_('Could not find story id in request.'))
    return HttpResponseServerError(_('Bad usage, please use a post request.'))


def delete_story_a(request, story_pk):
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

def delete_opinion(request):
    response = 'error'
    if request.POST:
        opinion = Opinion.objects.get(pk=request.POST.get('opinion_pk', None))
        if opinion:
            opinion.delete()
            response = 'OK'
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

def get_inline_select_field(request,relation_id,direction):
    story_relation = StoryRelation.objects.get(pk=relation_id)
    story_id = request.POST['value']
    story = Story.objects.get(pk = story_id)
    if direction == 'from':
        story_relation.from_story = story
    elif direction == 'to':
        story_relation.to_story = story

    story_relation.save()
    return HttpResponse("%s" % story.title)

def get_inline_select_json(request, discussion_pk, speech_act):
    result = []
    try:
        stories = Story.objects.filter(discussion = discussion_pk, speech_act__name = speech_act )
        result =  "{%s}" % ','.join(['"%s":"%s"' % (story.id,story.get_json_safe_title()) for story in stories])

    except:
        print sys.exc_info()
    #Return the response back
    return HttpResponse("%s"% result)

   # json = simplejson.dumps(['{"%s":"%s"}' % (story.id, story.title) for story in stories])

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
    opinion_types = SpeechAct.objects.filter(discussion_type=discussion.type, story_type=2)
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

def follow(request, discussion_slug):
    if request.user.is_authenticated():
        discussion = Discussion.objects.get(slug=discussion_slug)
        return _follow(request.user, discussion)
    else:
        return HttpResponse('error')

def unfollow(request, discussion_slug):
    if request.user.is_authenticated():
        discussion = Discussion.objects.get(slug=discussion_slug)
        return _unfollow(request.user, discussion)
    else:
        return HttpResponse('error')

def get_hints_metadata(discussion):
    metadata = get_workflow_hints(discussion)
    return simplejson.dumps(metadata)