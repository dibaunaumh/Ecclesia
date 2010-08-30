from django.http import HttpResponseRedirect, HttpResponse, Http404
from models import *
from ecclesia.discussions.models import Story, Discussion
import datetime

def update_presentation(request):
    """
    Update the presentation feilds of elements on the featured view
    """
    model_name = request.POST.get('model_name', None)
    timestamp = ''
    if model_name:
        model_class = globals()[model_name]
        pk = request.POST.get('pk', None)
        if pk:
            object = model_class.objects.get(pk=pk)
            #object.h = int(request.POST.get('h', object.h))
            #object.w = int(request.POST.get('w', object.w))
            object.x = int(request.POST.get('x', object.x))
            object.y = int(request.POST.get('y', object.y))
            object.save()
            last_changed = request.POST.get('last_changed', None)
            if last_changed:
                timestamp = object.updated_at if object.updated_at else datetime.datetime.now()
            print "Coordinates updated successfully."
        else:
            print "Object's pk not specified."
    else:
        print "Model name not specified."
    return HttpResponse(str(timestamp))


def _follow(user, followed_object):
    if user and followed_object:
        subscription = Subscription()
        subscription.user = user
        subscription.followed_object = followed_object
        subscription.save()
        return HttpResponse('success')
    else:
        return HttpResponse('error')