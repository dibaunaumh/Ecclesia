from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import gettext_lazy as _
from common.utils import get_domain

class SpeechAct(models.Model):
    """
    A type of speech act
    """
    name = models.CharField(_('action type'), max_length=100)
    
    class Meta:
        verbose_name = _('speech act')
        verbose_name_plural = _('speech acts')
    
    def get_absolute_url(self):
        return "http://%s/admin/discussion/speechact/%s/" % (get_domain(), self.id)
    
    def __unicode__(self):
        return self.name

class Story(models.Model):
    """
    A user story attached to some object
    """
    content = models.TextField(_('content'), help_text=_("The user content"))
    speech_act = models.ForeignKey(SpeechAct, verbose_name=_('speech act'), null=True, blank=True, help_text=_("The speech act of the story"))
    created_by = models.ForeignKey(User, verbose_name=_('created by'), null=True, blank=True, help_text=_('The user that made the speech'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, help_text=_('When the speech was made'))
    updated_at = models.DateTimeField(_('updated at'), auto_now=True, help_text=_('When the speech was last updated'))
    
    # Generic foreign key machinery follows
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    object = generic.GenericForeignKey() # Unfortunately, it does not support verbose_name and help_text, so no gettext here.
    
    class Meta:
        verbose_name = _('story')
        verbose_name_plural = _('stories')
    
    def get_absolute_url(self):
        return "http://%s/admin/discussion/story/%s/" % (get_domain(), self.id)
    
    def __unicode__(self):
        return _('Story #%s') % (self.id)
