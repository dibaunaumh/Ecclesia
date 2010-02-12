from django.http import HttpResponseRedirect, HttpResponse, Http404
from groups.models import *
from discussions.models import *

ENTITY_TYPES_MAP = { 'group': GroupProfile, 
					 'disc' : Discussion }

def update_presentation(request):
    """
    Update groups x and y positions on the featured view
    """
    model_name = request.POST.get('model_name', None)
    if model_name is not None:
        print model_name
        model_class = globals()[model_name]
        pk = request.POST.get('pk', None)
        if pk is not None:
            object = model_class.objects.get(pk=pk)
            msg = "Coordinates updated successfully."
            pos_x = 'x_%s' % object.pk
            pos_y = 'y_%s' % object.pk
            object.x_pos = int(request.POST.get(pos_x, object.x_pos))
            object.y_pos = int(request.POST.get(pos_y, object.y_pos))
            object.save()
        else:
            msg = "Object's pk not specified."
    else:
        msg = "Model name not specified."
    return HttpResponse(msg)

