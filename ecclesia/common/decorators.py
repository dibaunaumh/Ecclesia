from django.contrib import messages
from django.utils.translation import ugettext as _


def notify_not_logged_in(function=None):
    """
    Decorator for views that adds a message if the user isn't logged in
    """
    def wrapper(request, **kwargs):
        if (not request.user or not request.user.is_authenticated()):
            # add message to the user
            messages.add_message(request, messages.INFO, _("You need to login in order to make any changes"))

        return function(request, **kwargs)

    return wrapper




