from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from groups.models import *
from goals.models import *
from django.contrib.auth.models import Group, User


def home(request):
    """
    Renders the application home page
    """
    groups = GroupProfile.objects.all()
    user = request.user
    return render_to_response('home.html', locals())


def group_home(request, group_name):
    """
    Homepage of a group, displaying the group's description & active content.
    """
    user=request.user
    query = GroupProfile.objects.filter(name=group_name)
    if query.count() == 0:
        raise Http404("Can't find group named: %s" % group_name)
    else:
        group = query[0]
    query = group.mission_statements.all().order_by("-created_at")
    if query.count() > 0:
        mission_statement = query[0].mission_statement
    else:
        mission_statement = ""
    goals = group.goals.all()
    members = User.objects.filter(groups=group.group)
    user_in_group = False
    try:
        user_in_group = request.user.groups.filter(id=group.group.id).count() > 0
    except:
        pass
    return render_to_response('group_home.html', locals())



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


def is_in_group(request):
    if 'group_name' in request.GET:
        group = Group.objects.get(name=request.GET['group_name'])
        if request.user.groups.filter(id=group.id):
            return HttpResponse("True")
    return HttpResponse("False")
    
def join_group(request):
    if 'group_name' in request.POST:
        group = Group.objects.get(name=request.POST['group_name'])
        request.user.groups.add(group)
    return HttpResponse("")
    
def leave_group(request):
    if 'group_name' in request.POST:
        group = Group.objects.get(name=request.POST['group_name'])
        request.user.groups.remove(group)
    return HttpResponse("")

def login(request):
    path = request.POST['path']
    return render_to_response('admin/login.html', locals())