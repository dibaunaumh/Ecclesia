from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import gettext_lazy as _
from django.core import urlresolvers

SPEECH_ACT_CHOICES = (
                      # These are the types of speech acts available in the system:
                      (0, _('opinion')),
                      (1, _('support')),
                      (2, _('contradiction'))
                      #TODO: think of good items to put here and revise the list
                      )

class Story(models.Model):
    """
    A user story attached to some object
    """
    content = models.TextField(_('content'), help_text=_("The user content"))
    speech_act = models.SmallIntegerField(choices=SPEECH_ACT_CHOICES, verbose_name=_('speech act'), null=True, blank=True, help_text=_("The speech act of the story"))
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
        return urlresolvers.reverse('admin:discussion_story_change', args=(self.id,))
    
    def __unicode__(self):
        return _("%(user)s's %(speechact)s (#%(id)s)") % {'user':self.created_by.get_full_name(), 'speechact':self.get_speech_act_display(), 'id':self.id}

    def name_with_link(self):
        return _('<a href="%(url)s">%(user)s\'s %(speechact)s (#%(id)s)</a>') % {'user':self.created_by.get_full_name(), 'speechact':self.get_speech_act_display(), 'id':self.id, 'url':self.get_absolute_url()}
