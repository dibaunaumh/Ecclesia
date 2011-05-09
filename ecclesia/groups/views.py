import sys
import base64

from django.shortcuts import  render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseBadRequest
from django.core import serializers
from django.contrib import messages
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import simplejson

from groups.models import *
from discussions.models import *
from discussions.forms import DiscussionForm
from notifications.models import Notification
from forms import *
from services.search_filter_pagination import search_filter_paginate
from services.utils import get_user_permissions
from common.utils import is_heb, get_domain

def home(request):
    """
    Renders the application home page
    """
    user = request.user
    user_permissions = 'allowed' if user.is_authenticated() else ''
    if not user_permissions:
        return render_to_response('intro.html', locals(), context_instance=RequestContext(request))
    return HttpResponseRedirect("/groups/")

def groups(request):
    """
    Renders the groups home
    """
    groups = GroupProfile.objects.all()
    user = request.user
    user_permissions = 'allowed' if user.is_authenticated() else ''
    show_errors_in_form = False
    group_form = GroupProfileForm()
    return render_to_response('home.html', locals())

def get_groups_view_json(request):
    groups = GroupProfile.objects.all()
    json = ','
    for group in groups:
        json = '%s{"group":{"id":%s,"url":"%s","name":"%s","dimensions":{"x":%s,"y":%s,"w":%s,"h":%s}}},' % (
        json, group.id, group.get_absolute_url(), group.group.name, group.x, group.y, group.w, group.h)
    #json_serializer = serializers.get_serializer("json")()
    #json_serializer.serialize(groups, ensure_ascii=False, stream=response, fields=('x', 'y', 'w', 'h'))
    json = json.strip(',')
    return HttpResponse('[%s]' % json)

def get_discussions_view_json(request, group_slug):
    group_profile = GroupProfile.objects.get(slug=group_slug)
    group = group_profile.group
    discussions = Discussion.objects.filter(group=group)
    json = ','
    for discussion in discussions:
        json = '%s{"discussion":{"id":%s,"url":"%s","name":"%s","dimensions":{"x":%s,"y":%s,"w":%s,"h":%s}}},' % (
        json, discussion.id, discussion.get_absolute_url(), discussion.name, discussion.x, discussion.y, discussion.w,
        discussion.h)
    #json_serializer = serializers.get_serializer("json")()
    #json_serializer.serialize(groups, ensure_ascii=False, stream=response, fields=('x', 'y', 'w', 'h'))
    json = json.strip(',')
    return HttpResponse('[%s]' % json)

def add_group(request):
    if request.POST:
        name = request.POST.get('group_name', None)
        if name:
            try:
                if Group.objects.filter(name=name):
                    group = Group.objects.filter(name=name)[0]
                else:
                    group = Group(name=name)
                    group.save()
                group_profile = GroupProfile()
                group_profile.group = group
                if is_heb(name):
                    encoded_name = name.__repr__().encode("ascii")[2:-1]
                    group_profile.slug = slugify(encoded_name)
                else:
                    group_profile.slug = slugify(name)
                group_profile.description = request.POST.get('description', '')
                group_profile.created_by = request.user
                group_profile.x = request.POST.get('x', None)
                group_profile.y = request.POST.get('y', None)
                group_profile.is_private = True if 'is_private' in request.POST else False
                group_profile.save()
                return HttpResponse('reload')
            except:
                resp = HttpResponse(str(sys.exc_info()[1]))
                resp.status_code = 500
                return resp
        else:
            return HttpResponseBadRequest('No name provided')
    else:
        return HttpResponse('Wrong usage: HTTP POST expected')

def group_home(request, group_slug):
    """
    Homepage of a group, displaying the group's description & active content.
    """
    user = request.user
    group = GroupProfile.objects.get(slug=group_slug)
    user_permissions = ''
    if not group:
        raise Http404("Can't find a group with the slug: %s" % group_slug)
    else:
        user_permission_type = get_user_permissions(user, group)
        if user_permission_type != 3 and user_permission_type != "Not logged in":
            user_permissions = 'allowed'
    query = group.mission_statements.all().order_by("-created_at")
    if query.count() > 0:
        mission_statement = query[0]
    else:
        mission_statement = ""
    discussions = group.group.discussions.all()
    members = group.get_group_members()
    user_in_group = group.is_user_in_group(request.user)
    if group.is_private and not user_in_group:
        messages.error(request, "The group is private. You're not allowed to see it." )
    #initializing the forms
    discussion_form = DiscussionForm()
    mission_statement_form = MissionStatementForm()
    return render_to_response('group_home.html', locals(), context_instance=RequestContext(request))

def set_mission_statement(request, group_pk):
    result = ''
    if request.POST and group_pk:
        mission_statement = MissionStatement()
        mission_statement.group_profile = GroupProfile.objects.get(pk=group_pk)
#        mission_statement_form = MissionStatementForm(request.POST)
#        mission_statement.mission_statement = mission_statement_form.cleaned_data['mission_statement']
        mission_statement.mission_statement = request.POST.get('mission_statement', '')
        mission_statement.created_by = request.user
        mission_statement.save()
        result = mission_statement.mission_statement
    return HttpResponse(result)

def groups_list(request):
    groups = GroupProfile.objects.all()
    user = request.user
    (my_items, get_parameters, f) = search_filter_paginate('group', groups, request)
    return render_to_response('groups_list.html', locals())

def members_list(request, group_slug):
    query = GroupProfile.objects.filter(slug=group_slug)
    if query.count() == 0:
        raise Http404("Can't find group named: %s" % group_slug)
    else:
        group = query[0]
        user = request.user
        if str(user) != 'AnonymousUser':
            if GroupPermission.objects.filter(group=group).filter(user=user):
                permission = GroupPermission.objects.filter(group=group.group).filter(user=user)[0]
                user_permission_type = permission.permission_type
    members = group.group.user_set.all()
    (my_items, get_parameters, f) = search_filter_paginate('member', members, request)
    return render_to_response('members_list.html', locals())

def user_home(request, user_name):
    """
    Homepage of a user, displaying the user's description & active content.
    """
    query = User.objects.filter(username=user_name)
    if query.count() == 0:
        raise Http404("Can't find a user named: %s" % user_name)
    else:
        user = query[0]
        if UserProfile.objects.filter(user=user):
            user_profile = UserProfile.objects.filter(user=user)[0]
    groups = get_user_groups(user)
    return render_to_response('user_home.html', locals())


def edit_user_profile(request):
    """
    Allows a user to edit his profile.
    """
    user = request.user
    user_profile = UserProfile.objects.filter(user=user)[0]
    if request.method == 'POST':
        form = MemberProfileForm(request.POST)
        additional_form = MemberAdditionalProfileForm(request.POST)
        if form.is_valid() and additional_form.is_valid():
            cd = form.cleaned_data
            user.first_name = cd['first_name']
            user.last_name = cd['last_name']
            user.email = cd['email']
            user.save()
            if 'picture' in request.FILES:
                file = request.FILES['picture']
                user_profile.picture.save(file.name, file, save=True)
            user_profile.gravatar = additional_form.cleaned_data['gravatar']
            user_profile.save()
            return HttpResponseRedirect('/')
    else:
        form = MemberProfileForm(instance=request.user)
        additional_form = MemberAdditionalProfileForm(instance=user_profile)
    return render_to_response('edit_profile.html', locals())

def delete_picture(request):
    user_profile = UserProfile.objects.filter(user=request.user)[0]
    user_profile.picture = 'img/user_pics/default_photo.gif'
    user_profile.gravatar = None
    user_profile.save()
    return HttpResponseRedirect("/user-profile")

def is_in_group(request):
    if 'group_slug' in request.GET:
        group = GroupProfile.objects.get(slug=request.GET['group_slug'])
        if request.user.groups.filter(id=group.group.id):
            return HttpResponse("True")
    return HttpResponse("False")

def get_user_groups_by_im(request, user_im_address=None):
    profile = get_object_or_404(UserProfile, im_address=user_im_address)
    user = profile.user
    groups = [(g.id, g.name) for g in user.groups.all()]
    return HttpResponse(simplejson.dumps(groups))

def get_user_groups(user):
    return [group.profile.get() for group in user.groups.all()]

def get_group_members(request, group_pk):
    group = get_object_or_404(Group, pk=group_pk)
    only_IM_receivers = request.GET.get("only_IM_receivers", "True") == "True"
    only_not_connected = request.GET.get("only_not_connected", "True") == "True"
    users = User.objects.filter(groups=group)
    profiles = [user.profile.get() for user in users]
    if only_IM_receivers:
        members = [profile.im_address for profile in profiles if profile.im_address and profile.receive_im_notification]   # TODO check whether connected to Ekkli
    else:
        members = [profile.im_address for profile in profiles if profile.im_address]
    return HttpResponse(simplejson.dumps(members))


def join_group(request):
    if 'group_slug' in request.POST:
        group = GroupProfile.objects.get(slug=request.POST['group_slug'])
        if group.is_private:
            try:
                manager = GroupPermission.objects.filter(group=group.group, permission_type=1)[0].user
                key = base64.b64encode("%s_%s" % (request.user.pk, group.pk))
                notification = Notification(text = "User %s is asking your permission to join the group %s.\n \
                    Please click the following link if you approve:\n \
                    http://%s/approve/%s" % (request.user.username, group.group.name, get_domain(), key), entity=group, recipient = manager)
                notification.save()
                return HttpResponse("")
            except:
                pass
        request.user.groups.add(group.group)
        GroupPermission(group=group.group, user=request.user, permission_type=2).save()
        return HttpResponse("Joined")
    return HttpResponse("")

def leave_group(request):
    if 'group_slug' in request.POST:
        group = GroupProfile.objects.get(slug=request.POST['group_slug'])
        GroupPermission.objects.filter(group=group.group).filter(user=request.user).delete()
        request.user.groups.remove(group.group)
    return HttpResponse("")

def login(request):
    path = request.POST['path']
    return render_to_response('admin/login.html', locals())

def delete_group(request, group_pk):
    group_profile = GroupProfile.objects.get(pk=group_pk)
    group = group_profile.group
    group_profile.delete()
    group.delete()
    return HttpResponseRedirect('/')

def delete_member(request, group_pk, member_pk):
    group = GroupProfile.objects.get(pk=group_pk)
    member = User.objects.get(pk=member_pk)
    member.groups.remove(group.group)
    GroupPermission.objects.filter(group=group.group).filter(user=member).delete()
    return HttpResponseRedirect('/members_list/%s/' % group.group.slug)

def promote_member(request, group_pk, member_pk):
    group = GroupProfile.objects.get(pk=group_pk)
    member = User.objects.get(pk=member_pk)
    if GroupPermission.objects.filter(group=group.group).filter(user=member):
        permission = GroupPermission.objects.filter(group=group.group).filter(user=member)[0]
        if permission.permission_type > 1:
            permission.permission_type = permission.permission_type - 1
            permission.save()
    return HttpResponseRedirect('/members_list/%s/' % group.name)

def demote_member(request, group_pk, member_pk):
    group = GroupProfile.objects.get(pk=group_pk)
    member = User.objects.get(pk=member_pk)
    if GroupPermission.objects.filter(group=group.group).filter(user=member):
        permission = GroupPermission.objects.filter(group=group.group).filter(user=member)[0]
        if permission.permission_type < 3:
            permission.permission_type = permission.permission_type + 1
            permission.save()
    return HttpResponseRedirect('/members_list/%s/' % group.name)

def approve_user(request, approve_key):
    key = str(base64.b64decode(approve_key))
    user = get_object_or_404(User, pk = int(key.split("_")[0]))
    group = get_object_or_404(GroupProfile, pk = int(key.split("_")[1]))
    try:
        user.groups.add(group.group)
        GroupPermission(group=group.group, user=user, permission_type=2).save()
        messages.add_message(request, messages.INFO, "Your approval is successful!")
        notification = Notification(text = \
            "Manager of the group %s has just approved you to join.\n Click on the following link to go to that group: http://%s/group/%s/ \n \
            Have fun!" % (group.group.name, get_domain(), group.slug), entity=group, recipient = user)
        notification.save()
    except:
        pass
    return HttpResponseRedirect('/')



