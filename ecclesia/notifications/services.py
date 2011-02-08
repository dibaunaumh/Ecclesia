import sys

from models import Notification
from django.http import HttpResponse

def create_notification(text, entity, acting_user):
    try:
        notification = Notification(text = text, entity = entity, acting_user = acting_user)
        notification.save()
        return HttpResponse(_('Notification create successfully'))
    except:
        resp = HttpResponse(str(sys.exc_info()[1]))
        resp.status_code = 500
        return resp