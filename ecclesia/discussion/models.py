from django.db import models
from django.contrib.auth.models import User

class Story(models.Model):
    content = models.TextField(_('content'), max_length=10000)
    speech_act = models.ForeignKey(SpeechAct)
    created_by = models.ForeignKey(User, verbose_name=_('created by'), null=True, blank=True, help_text=_('The user that made the speech'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, help_text=_('When the speech was made'))
    updated_at = models.DateTimeField(_('updated at'), auto_now=True, help_text=_('When the speech was last updated'))
    #generic foreign key should be added
    