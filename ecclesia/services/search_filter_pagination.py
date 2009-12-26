from utils import get_query
from groups.forms import GroupProfileFilter, MemberProfileFilter
from django.core.paginator import Paginator, InvalidPage, EmptyPage

def search_filter_paginate(entity_name, all_objects, request):
    
    #search
    search_string = ""
    items_search = all_objects
    i = None
    if 'search' in request.GET and request.GET['search'].strip() != '':
        search_string = request.GET['search'].strip()
        if entity_name == 'group':
            i = get_query(request.GET['search'].strip(), ['name', 'description'])
        if entity_name == 'member':
            i = get_query(request.GET['search'].strip(), ['first_name', 'last_name', 'email'])
        items_search = all_objects.filter(i)
    
    #filter
    if entity_name == 'group':
        f = GroupProfileFilter(request.GET, queryset=items_search)
    if entity_name == 'member':
        f = MemberProfileFilter(request.GET, queryset=items_search)
    
    #pagination
    items_list = f.qs  
    paginator = Paginator(items_list, 20) # Show 20 items per page
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

    get_parameters = analyze_filters_parameters(entity_name, request)
    
    if 'search' in request.GET:
        if get_parameters == "?":
            get_parameters = "?search=%s" % request.GET['search']
        else:
            get_parameters = "%s&search=%s" % (get_parameters, request.GET['search'])
            
    return (my_items, get_parameters, f)

def analyze_filters_parameters(entity_name, request):
    get_parameters = "?"
    if entity_name == 'group':
        if 'parent' in request.GET:
            get_parameters = "?parent=%s&location=%s&created_by=%s&" % \
            (request.GET['parent'], request.GET['location'], request.GET['created_by'])
    if entity_name == 'member':
        if 'is_authenticated' in request.GET:
            get_parameters = "?is_active=%s&is_stuff=%s&is_superuser=%s&" % \
            (request.GET['is_active'], request.GET['is_stuff'], request.GET['is_superuser'])
    return get_parameters