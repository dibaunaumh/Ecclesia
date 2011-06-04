import sys

from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

from models import Notification

def create_notification(text, entity, acting_user=None, recipient = None):
    try:
        notification = Notification(text = text, entity = entity, acting_user = acting_user, recipient=recipient)
        notification.save()
        return HttpResponse(_('Notification create successfully'))
    except:
        resp = HttpResponse(str(sys.exc_info()[1]))
        resp.status_code = 500
        return resp