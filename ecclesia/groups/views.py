from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.core import serializers
from groups.models import *
from discussions.models import *
from discussions.forms import DiscussionForm
import sys
from forms import *

from django.contrib.auth.models import User
from services.search_filter_pagination import search_filter_paginate

def home(request):
    """
    Renders the application home page
    """
    groups = GroupProfile.objects.all()
    user = request.user
    #initializing the form
    show_errors_in_form = False
    group_form = GroupProfileForm()
    #saving new group
    if request.POST:
        group_form = GroupProfileForm(request.POST)
        if group_form.is_valid():
            save_group_from_form(group_form, request.user)
            group_form = GroupProfileForm()
        else:
            show_errors_in_form = True
    #adding beautiful css
    for key in group_form.fields:
        group_form.fields[key].widget.attrs["class"] = 'text ui-widget-content ui-corner-all'
    return render_to_response('home.html', locals())

def get_groups_view_json(request):
    groups = GroupProfile.objects.all()
    json = ',';
    for group in groups:
        json = '%s{"group":{"id":%s,"url":"%s","name":"%s","dimensions":{"x":%s,"y":%s,"w":%s,"h":%s}}},' % (json, group.id, group.get_absolute_url(), group.group.name, group.x, group.y, group.w, group.h)
    #json_serializer = serializers.get_serializer("json")()
    #json_serializer.serialize(groups, ensure_ascii=False, stream=response, fields=('x', 'y', 'w', 'h'))
    json = json.strip(',')
    return HttpResponse('[%s]' % json)

def get_discussions_view_json(request, group_slug):
    group = GroupProfile.objects.get(slug=group_slug).group
    discussions = Discussion.objects.filter(group=group)
    json = ',';
    for discussion in discussions:
        json = '%s{"discussion":{"id":%s,"url":"%s","name":"%s","dimensions":{"x":%s,"y":%s,"w":%s,"h":%s}}},' % (json, discussion.id, discussion.get_absolute_url(), discussion.name, discussion.x, discussion.y, discussion.w, discussion.h)
    #json_serializer = serializers.get_serializer("json")()
    #json_serializer.serialize(groups, ensure_ascii=False, stream=response, fields=('x', 'y', 'w', 'h'))
    json = json.strip(',')
    return HttpResponse('[%s]' % json)

def save_group_from_form(group_form, user):
    if Group.objects.filter(name=group_form.cleaned_data['slug']):
        group = Group.objects.filter(name=group_form.cleaned_data['slug'])[0]
    else:
        group = Group(name=group_form.cleaned_data['slug'])
        group.save()
    group_profile = GroupProfile()
    group_profile.group = group
    group_profile.slug = group_form.cleaned_data['slug']
    group_profile.description = group_form.cleaned_data['description']
    group_profile.created_by = user
    group_profile.save()
    return

def group_home(request, group_slug):
    """
    Homepage of a group, displaying the group's description & active content.
    """
    user=request.user
    query = GroupProfile.objects.filter(slug=group_slug)
    if query.count() == 0:
        raise Http404("Can't find a group with the slug: %s" % group_slug)
    else:
        group = query[0]
        if str(user) != 'AnonymousUser':
            if GroupPermission.objects.filter(group=group.group).filter(user=user):
                permission = GroupPermission.objects.filter(group=group.group).filter(user=user)[0]
                user_permission_type = permission.permission_type
    query = group.mission_statements.all().order_by("-created_at")
    if query.count() > 0:
        mission_statement = query[0]
    else:
        mission_statement = ""
    discussions = group.group.discussions.all()
    members = group.get_group_members()
    user_in_group = False
    try:
        user_in_group = request.user.groups.filter(id=group.group.id).count() > 0
    except:
        pass
    #initializing the forms
    show_errors_in_form = False
    show_errors_in_mission_statement_form = False
    discussion_form = DiscussionForm()
    mission_statement_form = MissionStatementForm()
    #saving new discussion
    if request.POST:
        if 'slug' in request.POST:
            discussion_form = DiscussionForm(request.POST)
            if discussion_form.is_valid():
                save_discussion_from_form(discussion_form, group, user)
                discussion_form = DiscussionForm()
            else:
                show_errors_in_form = True
        else:
            mission_statement_form = MissionStatementForm(request.POST)
            if mission_statement_form.is_valid():
                save_mission_statement_from_form(mission_statement_form, group, user)
                mission_statement_form = DiscussionForm()
            else:
                show_errors_in_mission_statement_form = True
    #adding beautiful css
    for key in discussion_form.fields:
        discussion_form.fields[key].widget.attrs["class"] = "text ui-widget-content ui-corner-all"
    for key in mission_statement_form.fields:
        mission_statement_form.fields[key].widget.attrs["class"] = "text ui-widget-content ui-corner-all"
    #last_related_update = str(group.last_related_update) # set an initial value for the update timestamp
    return render_to_response('group_home.html', locals())

def save_discussion_from_form(discussion_form, group, user):
    discussion = Discussion()
    discussion.group = group.group
    discussion.name = discussion_form.cleaned_data['name']
    discussion.slug = discussion_form.cleaned_data['slug']
    discussion.type = discussion_form.cleaned_data['type']
    discussion.description = discussion_form.cleaned_data['description']
    discussion.created_by = user
    discussion.save()
    return

def save_mission_statement_from_form(mission_statement_form, group, user):
    mission_statement = MissionStatement()
    mission_statement.group_profile = group
    mission_statement.mission_statement = mission_statement_form.cleaned_data['mission_statement']
    mission_statement.created_by = user
    mission_statement.save()
    return

def groups_list(request):
    groups = GroupProfile.objects.all()
    (my_items, get_parameters, f) = search_filter_paginate('group', groups, request)
    return render_to_response('groups_list.html', locals())

def members_list(request, group_slug):
    query = GroupProfile.objects.filter(slug=group_slug)
    if query.count() == 0:
        raise Http404("Can't find group named: %s" % group_slug)
    else:
        group = query[0]
        user=request.user
        if str(user) != 'AnonymousUser':
            if GroupPermission.objects.filter(group=group).filter(user=user):
                permission = GroupPermission.objects.filter(group=group.group).filter(user=user)[0]
                user_permission_type = permission.permission_type
    members = group.get_group_members()
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

def join_group(request):
    if 'group_slug' in request.POST:
        group = GroupProfile.objects.get(slug=request.POST['group_slug'])
        request.user.groups.add(group.group)
        GroupPermission(group=group.group, user=request.user, permission_type=2).save()
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