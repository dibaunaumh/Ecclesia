from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from groups.models import *
from goals.models import *

#imports for search, filter and pagination
from django.contrib.auth.models import Group, User
from utils import get_query
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from forms import GroupProfileFilter

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

def groups_list(request):
    groups = GroupProfile.objects.all()
    
    #search
    search_string = ""
    items_search = groups
    i = None
    if 'search' in request.GET and request.GET['search'].strip() != '':
        search_string = request.GET['search'].strip()
        i = get_query(request.GET['search'].strip(), ['name', 'description'])
        items_search = GroupProfile.objects.filter(i)
    
    #filter
    f = GroupProfileFilter(request.GET, queryset=items_search)
    
    #pagination
    items_list = f.qs  
    paginator = Paginator(items_list, 20) # Show 25 contacts per page
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    # If page request (9999) is out of range, deliver last page of results.
    try:
        my_items = paginator.page(page)
    except (EmptyPage, InvalidPage):
        my_items = paginator.page(paginator.num_pages)

    get_parameters = "?"
    if 'parent' in request.GET:
        get_parameters = "?parent=%s&location=%s&created_by=%s&" % \
        (request.GET['parent'], request.GET['location'], request.GET['created_by'])
    if 'search' in request.GET:
        if get_parameters == "?":
            get_parameters = "?search=%s" % request.GET['search']
        else:
            get_parameters = "%s&search=%s" % (get_parameters, request.GET['search'])
            
    return render_to_response('groups_list.html', locals())

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
    
    