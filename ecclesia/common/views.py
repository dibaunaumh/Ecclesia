from django.http import HttpResponseRedirect, HttpResponse, Http404
from groups.models import *
from discussions.models import *

ENTITY_TYPES_MAP = { 'group': GroupProfile, 
					 'disc' : Discussion }

def update_coords(request, entity_type):
    """
    Update groups x and y positions on the featured view
    """
    print entity_type
    elements = ENTITY_TYPES_MAP[entity_type]
    elements = elements.objects.all()
    msg = "Coordinates updated successfully."
    for element in elements:
        pos_x = 'x_%s' % element.pk
        pos_y = 'y_%s' % element.pk
        element.x_pos = int(request.POST.get(pos_x, element.x_pos))
        element.y_pos = int(request.POST.get(pos_y, element.y_pos))
        element.save()
       
    return HttpResponse(msg)

