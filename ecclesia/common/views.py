from django.http import HttpResponseRedirect, HttpResponse, Http404
from groups.models import *
from discussions.models import *

ENTITY_TYPES_MAP = { 'group': GroupProfile, 
					 'disc' : Discussion }

def update_presentation(request):
    """
    Update the presentation feilds of elements on the featured view
    """
    model_name = request.POST.get('model_name', None)
    if model_name is not None:
        model_class = globals()[model_name]
        pk = request.POST.get('pk', None)
        if pk is not None:
            object = model_class.objects.get(pk=pk)
            object.x = int(request.POST.get('x', object.x))
            object.y = int(request.POST.get('y', object.y))
            object.save()
            print "Coordinates updated successfully."
        else:
            print "Object's pk not specified."
    else:
        print "Model name not specified."
    return HttpResponse('OK')

