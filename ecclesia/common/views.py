from django.http import HttpResponseRedirect, HttpResponse, Http404
from groups.models import *
from discussions.models import *

def update_coords(request, entity_type):
    """
    Update groups x and y positions on the featured view
    """
	#do switch here
    elements = GroupProfile.objects.all()
    msg = "Coordinates updated successfully."
    for element in elements:
        pos_x = 'x_%s' % element.id
        pos_y = 'y_%s' % element.id
        element.x_pos = int(request.POST.get(pos_x, element.x_pos))
        element.y_pos = int(request.POST.get(pos_y, element.y_pos))
        element.save()
       
    return HttpResponse(msg)

