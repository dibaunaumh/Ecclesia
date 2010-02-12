from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import gettext_lazy as _
from django.core import urlresolvers
from groups.models import GroupProfile
from common.models import Presentable
from common.utils import get_domain

SPEECH_ACT_CHOICES = (
                      # These are the types of speech acts available in the system:
                      (0, _('opinion')),
                      (1, _('support')),
                      (2, _('contradiction'))
                      #TODO: think of good items to put here and revise the list
                      )


class DiscussionType(models.Model):
    name = models.CharField(_('name'), max_length=50, unique=True, blank=False, help_text=_('The name of the discussion type.'))

    class Meta:
        verbose_name = _('discussion type')
        verbose_name_plural = _('discussion types')
    
    def __unicode__(self):
        return self.name


class Discussion(Presentable):
    """
    A discussion between users, related to a group
    """
    group = models.ForeignKey(Group, verbose_name=_('group'), related_name='discussions', help_text=_("The group profile containing this discussion."))
    name = models.CharField(_('name'), max_length=50, help_text=_('The name of the discussion.'))
    slug = models.SlugField(_('slug'), unique=True, blank=False, help_text=_("The url representation of the discussion's name. No whitespaces allowed - use hyphen/underscore to separate words"))
    type = models.ForeignKey(DiscussionType, verbose_name=_('discussion type'), related_name='objects', help_text=_("The discussion's type."))
    description = models.CharField(_('short description'), max_length=500, null=True, blank=True, help_text=_('A short description of the discussion.'))
    # no nesting on this release...
	#parent = models.ForeignKey('self', verbose_name=_('parent'), related_name='children', null=True, blank=True, help_text=_('The parent discussion containing this discussion.'))
    # keeping it simple...
    #forked_from = models.ForeignKey('self', verbose_name=_('forked from'), related_name='forks', null=True, blank=True, help_text=_('The discussion from which this discussion forked.'))
    created_by = models.ForeignKey(User, verbose_name=_('created by'), null=True, blank=True, help_text=_('The user that created the discussion.'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, help_text=_('When was the discussion created.'))
    updated_at = models.DateTimeField(_('updated at'), auto_now=True, help_text=_('When was the discussion last updated.'))

    class Meta:
        verbose_name = _('discussion')
        verbose_name_plural = _('discussions')
        
    
    def get_absolute_url(self):
        return "http://%s/discussions/%s/" % (get_domain(), self.slug)
    
    def __unicode__(self):
        return self.name


class SpeechAct(models.Model):
    name = models.CharField(_('name'), max_length=50, unique=True, blank=False, help_text=_('The name of the speech act.'))

    def __unicode__(self):
        return self.name

		
class Story(Presentable):
    """
    A user story attached to a discussion
    """
    discussion = models.ForeignKey(Discussion, related_name='stories', verbose_name=_('discussion'), null=False, blank=False, help_text=_('The discussion this story is a part of.'))
    title = models.CharField(_('title'), max_length=50, blank=False, help_text=_('A title for story.'))
    slug = models.SlugField(_('slug'), max_length=50, unique=True, blank=False, help_text=_("The url representation of the story's title. No whitespaces allowed - use hyphen/underscore to separate words"))
    content = models.TextField(_('content'), help_text=_("The user content"))
    speech_act = models.ForeignKey(SpeechAct, related_name='objects', verbose_name=_('speech act'), null=False, blank=False, help_text=_("Which speech act this story represents."))
    created_by = models.ForeignKey(User, verbose_name=_('created by'), null=False, blank=False, help_text=_('The user that made the speech act.'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, help_text=_('When the speech act was made.'))
    updated_at = models.DateTimeField(_('updated at'), auto_now=True, help_text=_('When the speech act was last updated.'))
    
    # Generic foreign key machinery follows
    # content_type = models.ForeignKey(ContentType)
    # object_id = models.PositiveIntegerField()
    # object = generic.GenericForeignKey() # Unfortunately, it does not support verbose_name and help_text, so no gettext here.
    
    class Meta:
        verbose_name = _('story')
        verbose_name_plural = _('stories')
    
    def get_absolute_url(self):
        return "http://%s/story/%s/" % (get_domain(), self.slug)
    
    def __unicode__(self):
        return _("%(user)s's %(speechact)s (#%(id)s)") % {'user':self.created_by.get_full_name(), 'speechact':self.speech_act.name, 'id':self.id}

    def name_with_link(self):
        return _('<a href="%(url)s">%(user)s\'s %(speechact)s (#%(id)s)</a>') % {'user':self.created_by.get_full_name(), 'speechact':self.speech_act.name, 'id':self.id, 'url':self.get_absolute_url()}


class StoryRelation(Story):
    from_story = models.ForeignKey(Story, related_name='from_relation', verbose_name=_('from_relation'), null=False, blank=False, help_text=_('The story this story relation flows from.'))
    to_story = models.ForeignKey(Story, related_name='to_relation', verbose_name=_('to_relation'), null=False, blank=False, help_text=_('The story this story relation directs to.'))


class Opinion(Story):
    parent_story = models.ForeignKey(Story, related_name='opinions', verbose_name=_('parent story'), null=False, blank=False, help_text=_('The parent story containing this opinion.'))