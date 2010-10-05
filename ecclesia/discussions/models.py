from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
import datetime
from discussion_actions import evaluate_stories
from common.models import Presentable, Subscription
from common.utils import get_domain
import re
from ecclesia.groups.models import GroupProfile


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
    group = models.ForeignKey(Group, editable=False, verbose_name=_('group'), related_name='discussions', help_text=_("The group profile containing this discussion."))
    name = models.CharField(_('name'), max_length=50, help_text=_('The name of the discussion.'))
    slug = models.SlugField(_('slug'), max_length=500, unique=True, blank=False, help_text=_("The url representation of the discussion's name. No whitespaces allowed - use hyphen/underscore to separate words"))
    type = models.ForeignKey(DiscussionType, verbose_name=_('discussion type'), related_name='discussions', help_text=_("The discussion's type."))
    description = models.TextField(_('short description'), max_length=500, null=True, blank=True, help_text=_('A short description of the discussion.'))
    # no nesting on this release...
	#parent = models.ForeignKey('self', verbose_name=_('parent'), related_name='children', null=True, blank=True, help_text=_('The parent discussion containing this discussion.'))
    # keeping it simple...
    #forked_from = models.ForeignKey('self', verbose_name=_('forked from'), related_name='forks', null=True, blank=True, help_text=_('The discussion from which this discussion forked.'))
    created_by = models.ForeignKey(User, editable=False, verbose_name=_('created by'), null=True, blank=True, help_text=_('The user that created the discussion.'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, help_text=_('When was the discussion created.'))
    updated_at = models.DateTimeField(_('updated at'), auto_now=True, help_text=_('When was the discussion last updated.'))
    subscriptions = generic.GenericRelation(Subscription)

    class Meta:
        verbose_name = _('discussion')
        verbose_name_plural = _('discussions')


    def get_absolute_url(self):
        return "http://%s/discussions/discussion/%s/" % (get_domain(), self.slug)

    def get_visual_container(self):
        return self.group

    def __unicode__(self):
        return self.name


class SpeechAct(models.Model):
    name = models.SlugField(_('name'), max_length=50, blank=False, help_text=_('The name of the speech act.'))
    discussion_type = models.ForeignKey(DiscussionType, verbose_name=_('discussion type'), related_name='speech_acts', help_text=_('The type of discussion that allows this speech act.'))
    story_type = models.IntegerField(_('story type'), default=1, choices=((1,_('story')),(2,_('opinion')),(3,_('relation'))))
    ordinal = models.IntegerField(_('DOM ordinal'), default=0, help_text=_('Order of appearance of this speech act in the DOM.'))
    icon = models.ImageField(_('icon'), max_length=100, upload_to='img/speech_act_icons', null=True, blank=True, help_text=_('The name of the image file.'))

    def __unicode__(self):
        return self.name


class BaseStory(Presentable):
    title = models.CharField(_('title'), max_length=500, blank=True, null=False, help_text=_('A title for this story.'))
    slug = models.SlugField(_('slug'), max_length=500, blank=False, help_text=_("The url representation of the story's title. No whitespaces allowed - use hyphen/underscore to separate words"))
    content = models.TextField(_('content'), help_text=_("The user content"))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, help_text=_('When the speech act was made.'))
    updated_at = models.DateTimeField(_('updated at'), auto_now=True, help_text=_('When the speech act was last updated.'))
    created_by = models.ForeignKey(User, verbose_name=_('created by'), null=False, blank=False, help_text=_('The user that made the speech act.'))
	
    class Meta:
        abstract = True

    def get_children(self):
        return self.opinions.all()

    def get_children_js_array(self):
        children = self.get_children()
        if len(children):
            return '["%s"]' % '","'.join([child.unique_id() for child in children])
        else:
            return '[]'

    def get_json_safe_content(self):
        p = re.compile('(\n)')
        return p.sub(' ', self.content)

    def get_visual_container(self):
        return self.discussion


class Opinion(BaseStory):
    discussion = models.ForeignKey(Discussion, related_name='opinions', verbose_name=_('discussion'), null=False, blank=False, help_text=_('The discussion this story is a part of.'))
    speech_act = models.ForeignKey(SpeechAct, related_name='opinions', verbose_name=_('speech act'), null=False, blank=False, help_text=_("Which speech act this story represents."))
    #parent_story = models.ForeignKey(Story, related_name='opinions', verbose_name=_('parent story'), null=False, blank=False, help_text=_('The parent story containing this opinion.'))
    # Generic foreign key machinery follows
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    parent_story = generic.GenericForeignKey('content_type', 'object_id')
    # Unfortunately, it does not support verbose_name and help_text, so no gettext here.
    opinions = generic.GenericRelation('self')

    class Meta:
        verbose_name = _('opinion')
        verbose_name_plural = _('opinions')
        unique_together = (('discussion', 'slug'),)

    def unique_id(self):
        return "%s_%d" % ('opinion', self.id)

    def get_absolute_url(self):
        return "http://%s/discussions/%s/opinion/%s/" % (get_domain(), self.discussion.slug, self.slug)

    def __unicode__(self):
        return self.title


class Story(BaseStory):
    """
    A user story attached to a discussion
    """
    discussion = models.ForeignKey(Discussion, related_name='stories', verbose_name=_('discussion'), null=False, blank=False, help_text=_('The discussion this story is a part of.'))
    speech_act = models.ForeignKey(SpeechAct, related_name='stories', verbose_name=_('speech act'), null=False, blank=False, help_text=_("Which speech act this story represents."))
    parent = models.ForeignKey("Story", default=None, related_name='parent story', verbose_name=_('parent'), null=True, blank=True, help_text=_("Parent story if the story belong to story group"))
    is_parent = models.BooleanField(default=False, verbose_name=_('is parent'), help_text=_("Boolean field that tells us if the story is a parent of stories group"))
    opinions = generic.GenericRelation(Opinion)

    class Meta:
        verbose_name = _('story')
        verbose_name_plural = _('stories')
        unique_together = (('discussion', 'slug'),)

    def unique_id(self):
        return "%s_%d" % ('story', self.id)
		
    def get_absolute_url(self):
        return "http://%s/discussions/%s/story/%s/" % (get_domain(), self.discussion.slug, self.slug)

    def __unicode__(self):
        return self.title
        #return _("%(title) - %(user)s's %(speechact)s (#%(id)s)") % {'title': self.title, 'user':self.created_by.get_full_name(), 'speechact':self.speech_act.name, 'id':self.id}

    def name_with_link(self):
        return _('<a href="%(url)s">%(user)s\'s %(speechact)s (#%(id)s)</a>') % {'user':self.created_by.get_full_name(), 'speechact':self.speech_act.name, 'id':self.id, 'url':self.get_absolute_url()}


class StoryRelation(BaseStory):
    discussion = models.ForeignKey(Discussion, related_name='relations', verbose_name=_('discussion'), null=False, blank=False, help_text=_('The discussion this story is a part of.'))
    speech_act = models.ForeignKey(SpeechAct, related_name='relations', verbose_name=_('speech act'), null=False, blank=False, help_text=_("Which speech act this story represents."))
    from_story = models.ForeignKey(Story, related_name='from_relation', verbose_name=_('from_relation'), null=False, blank=False, help_text=_('The story this story relation flows from.'))
    to_story = models.ForeignKey(Story, related_name='to_relation', verbose_name=_('to_relation'), null=False, blank=False, help_text=_('The story this story relation directs to.'))
    opinions = generic.GenericRelation(Opinion)

    class Meta:
        verbose_name = _('story relation')
        verbose_name_plural = _('story relations')
        unique_together = (('discussion', 'slug'),)

    def unique_id(self):
        return "%s_%d" % ('relation', self.id)
		
    def get_absolute_url(self):
        return "http://%s/discussions/%s/relation/%s/" % (get_domain(), self.discussion.slug, self.slug)

    def __unicode__(self):
        return self.title


class DiscussionConclusion(models.Model):
    discussion = models.ForeignKey(Discussion, verbose_name=_("discussion"))
    story = models.ForeignKey(Story, verbose_name=_("story"))
    score = models.IntegerField()
    updated_at = models.DateTimeField(_('updated at'), auto_now=True, help_text=_('When the speech act was last updated.'))

    class Meta:
        verbose_name = _("discussion conclusion")
        verbose_name_plural = _("discussion conclusions")

    def __unicode__(self):
        return "Discussion conclusion of %s" % self.discussion


def last_changed_updater(sender, instance, **kwargs):
    container = sender.get_visual_container(instance)
    container.last_related_update = instance.updated_at if hasattr(instance, 'updated_at') else datetime.datetime.now()
    container.save()
    if isinstance(container, Discussion):
        evaluate_stories(instance.discussion)


# connecting post_save signal of stories and opinions to update their parent discussion's last_related_update field 
models.signals.post_save.connect(last_changed_updater, sender=Story)
models.signals.post_save.connect(last_changed_updater, sender=Opinion)
models.signals.post_save.connect(last_changed_updater, sender=StoryRelation)
models.signals.post_save.connect(last_changed_updater, sender=Discussion)