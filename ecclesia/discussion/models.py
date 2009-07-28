from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Story(models.Model):
    content = models.TextField(_('content'), max_length=10000, help_text=_("The content of the story"))
    #SpeechAct class should be defined
    #speech_act = models.ForeignKey('SpeechAct', verbose_name=_('speech_act'), null=True, blank=True, help_text=_("The speach act of the story"))
    created_by = models.ForeignKey(User, verbose_name=_('created by'), null=True, blank=True, help_text=_('The user that made the speech'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, help_text=_('When the speech was made'))
    updated_at = models.DateTimeField(_('updated at'), auto_now=True, help_text=_('When the speech was last updated'))
    #generic foreign key should be added
    