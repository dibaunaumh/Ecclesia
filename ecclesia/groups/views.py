from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from groups.models import *
from discussions.models import *
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
    return render_to_response('home.html', locals())


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
            if GroupPermission.objects.filter(group=group).filter(user=user):
                permission = GroupPermission.objects.filter(group=group).filter(user=user)[0]
                user_permission_type = permission.permission_type
    query = group.mission_statements.all().order_by("-created_at")
    if query.count() > 0:
        mission_statement = query[0].mission_statement
    else:
        mission_statement = ""
<<<<<<< HEAD
    discussions = group.discussions.all()
    members = User.objects.filter(groups=group.group)
=======
    goals = group.goals.all()
    members = User.objects.filter(groups=group.group)  
>>>>>>> origin/master
    user_in_group = False
    try:
        user_in_group = request.user.groups.filter(id=group.group.id).count() > 0
    except:
        pass
    return render_to_response('group_home.html', locals())

def groups_list(request):
    groups = GroupProfile.objects.all()
    (my_items, get_parameters, f) = search_filter_paginate('group', groups, request)
    return render_to_response('groups_list.html', locals())

def members_list(request, group_name):
    query = GroupProfile.objects.filter(name=group_name)
    if query.count() == 0:
        raise Http404("Can't find group named: %s" % group_name)
    else:
        group = query[0]
    members = User.objects.filter(groups=group.group)
    (my_items, get_parameters, f) = search_filter_paginate('member', members, request)
    return render_to_response('members_list.html', locals())

def update_coords(request):
    """
    Update groups x and y positions on the featured view
    """
    groups = GroupProfile.objects.all()
    msg = "Coordinates updated successfully."
    for group in groups:
        pos_x = 'x_%s' % group.id
        pos_y = 'y_%s' % group.id
        group.x_pos = int(request.POST.get(pos_x, group.x_pos))
        group.y_pos = int(request.POST.get(pos_y, group.y_pos))
        group.save()
       
    return HttpResponse(msg)
	
def user_home(request, user_name):
    """
    Homepage of a user, displaying the user's description & active content.
    """
    query = User.objects.filter(username=user_name)
    if query.count() == 0:
        raise Http404("Can't find a user named: %s" % user_name)
    else:
        user = query[0]
    groups = get_user_groups(user)
    return render_to_response('user_home.html', locals())


def edit_user_profile(request, user_name):
    """
    Allows a user to edit her profile.
    """
    user = request.user
    if request.method == 'POST':
        form = MemberProfileForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user.first_name = cd['first_name']
            user.last_name = cd['last_name']
            user.email = cd['email']
            user.save()
            return HttpResponseRedirect('/')
    else:
        form = MemberProfileForm(instance=request.user)
    return render_to_response('edit_profile.html', {'form': form})


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
        GroupPermission(group=group, user=request.user, permission_type=2).save()
    return HttpResponse("")
    
def leave_group(request):
    if 'group_slug' in request.POST:
        group = GroupProfile.objects.get(slug=request.POST['group_slug'])
        GroupPermission.object.filter(group=group).filter(user=request.user).delete()
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
    GroupPermission.objects.filter(group=group).filter(user=member).delete()
    return HttpResponseRedirect('/group/%s/' % group.slug)

def promote_member(request, group_pk, member_pk):
    group = GroupProfile.objects.get(pk=group_pk)
    member = User.objects.get(pk=member_pk)
    if GroupPermission.objects.filter(group=group).filter(user=member):
        permission = GroupPermission.objects.filter(group=group).filter(user=member)[0]
        if permission.permission_type > 1:
            permission.permission_type = permission.permission_type - 1
            permission.save()
    return HttpResponseRedirect('/group/%s/' % group.slug)

def demote_member(request, group_pk, member_pk):
    group = GroupProfile.objects.get(pk=group_pk)
    member = User.objects.get(pk=member_pk)
    if GroupPermission.objects.filter(group=group).filter(user=member):
        permission = GroupPermission.objects.filter(group=group).filter(user=member)[0]
        if permission.permission_type < 3:
            permission.permission_type = permission.permission_type + 1
            permission.save()
    return HttpResponseRedirect('/group/%s/' % group.slug)