from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

class Presentable(models.Model):
    x = models.IntegerField(default=0, editable=False, verbose_name=_('x position'), help_text=_('Horizontal posinition in view from left border.'))
    y = models.IntegerField(default=0, editable=False, verbose_name=_('y position'), help_text=_('Vertical posinition in view from top border.'))
    w = models.IntegerField(default=150, editable=False, verbose_name=_('width'), help_text=_("Object's width."))
    h = models.IntegerField(default=100, editable=False, verbose_name=_('height'), help_text=_("Object's height."))
    last_related_update = models.DateTimeField(_('related last updated at'), null=True, auto_now_add=True, help_text=_('When was the object\'s elements last updated.'))

    class Meta:
        abstract = True


class Subscription(models.Model):
    """
    Users' subscriptions to get notifictions on objects (follow)
    """
    user = models.ForeignKey(User, verbose_name=_('user'), related_name='subscriptions', null=False, blank=False, help_text=_('The subscribed user.'))
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    followed_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return '%s\'s follow on %s' % (self.user, followed_object)