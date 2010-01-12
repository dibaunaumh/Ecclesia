from ecclesia.discussions.models import Story, Discussion
from ecclesia.groups.models import GroupProfile, GroupPermission
from ecclesia.discussions.forms import StoryForm
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect

from services.search_filter_pagination import search_filter_paginate

def submit_story(request):
    story = Story(created_by=request.user)
    form = StoryForm(request.POST, instance=story)
    try:
        form.save()
    except ValueError:
        return render_to_response('write_story_miniform.html', {'form':form})
    return HttpResponse('OK')

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
    return HttpResponseRedirect('/discussions_list/%s/' % group.name)