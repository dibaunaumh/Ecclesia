from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from groups.models import *
from django.contrib.auth.models import Group


def home(request):
    """Renders the application home page"""
    groups = GroupProfile.objects.all()
    return render_to_response('home.html', locals())

def is_in_group(request):
    if 'group_id' in request.GET:
        group = Group.objects.get(id=request.GET['group_id'])
        if request.user.groups.filter(id=group.id):
            return HttpResponse("True")
    return HttpResponse("False")
    
def join_group(request):
    if 'group_id' in request.POST:
        group = Group.objects.get(id=request.POST['group_id'])
        request.user.groups.add(group)
    return HttpResponse("")
    
def leave_group(request):
    if 'group_id' in request.POST:
        group = Group.objects.get(id=request.POST['group_id'])
        request.user.groups.remove(group)
    return HttpResponse("")