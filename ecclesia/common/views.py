from django.http import HttpResponseRedirect, HttpResponse, Http404
from models import *
from ecclesia.discussions.models import Story, Discussion
from ecclesia.groups.models import GroupProfile
import datetime

def update_presentation(request):
    """
    Update the presentation feilds of elements on the featured view
    """
    model_name = request.POST.get('model_name', None)
    update_time = False
    timestamp = datetime.datetime.now()
    if model_name:
        model_class = globals()[model_name]
        pk = request.POST.get('pk', None)
        if pk:
            object = model_class.objects.get(pk=pk)
            if object and hasattr(object, 'discussion') and hasattr(object.discussion, 'last_related_update'):
                last_changed = request.POST.get('last_changed', None)
                if last_changed:
                    try:
                        last_changed_datetime = datetime.datetime.strptime(last_changed, '%Y-%m-%d %H:%M:%S.%f')
                    except:
                        last_changed_datetime = datetime.datetime.strptime(last_changed, '%Y-%m-%d %H:%M:%S')
                    if last_changed_datetime < object.discussion.last_related_update:
                        timestamp = last_changed
                    else:
                        update_time = True
                else:
                    timestamp = datetime.datetime.now()
            #object.h = int(request.POST.get('h', object.h))
            #object.w = int(request.POST.get('w', object.w))
            object.x = int(request.POST.get('x', object.x))
            object.y = int(request.POST.get('y', object.y))
            object.save()
            print "Coordinates updated successfully."
        else:
            print "Object's pk not specified."
    else:
        print "Model name not specified."
    if update_time:
        timestamp = object.updated_at if hasattr(object, 'updated_at') else timestamp
    return HttpResponse(str(timestamp))

def presentation_status(request, model_name, object_pk):
    datetime_format = '%Y-%m-%d %H:%M:%S.%f'
    last_changed_client = request.POST.get('last_changed', None)
    last_changed_db = ''
    try:
        model_class = globals()[model_name]
    except:
        return Http404()
    if model_class:
        object = model_class.objects.get(pk=object_pk)
        if object and hasattr(object, 'last_related_update'):
            last_changed_db = object.last_related_update
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

def _follow(user, followed_object):
    if user and followed_object:
        subscription = Subscription()
        subscription.user = user
        subscription.followed_object = followed_object
        subscription.save()
        return HttpResponse('success')
    else:
        return HttpResponse('error')