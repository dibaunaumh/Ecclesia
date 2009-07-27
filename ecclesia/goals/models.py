from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from common.utils import get_domain
from groups.models import GroupProfile


class Goal(models.Model):
    """
    An agreed goal of a group.
    """
    group_profile = models.ForeignKey(GroupProfile, verbose_name=_('group profile'), help_text=_("The goal's group"))
    name = models.SlugField(_('name'), help_text=_('The name of the goal. No whitespaces allowed - use hyphen to separate words.'))
    short_description = models.CharField(_('short description'), max_length=500, help_text=_('A short description of the goal.'))
    parent = models.ForeignKey('self', verbose_name=_('parent'), related_name='children', null=True, blank=True, help_text=_('The parent goal containing this goal'))
    forked_from = models.ForeignKey('self', verbose_name=_('forked from'), related_name='forks', null=True, blank=True, help_text=_('The goal from which this goal forked'))
    #tags
    created_by = models.ForeignKey(User, verbose_name=_('created by'), null=True, blank=True, help_text=_('The user that created the goal'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, help_text=_('When was the goal created'))
    updated_at = models.DateTimeField(_('updated at'), auto_now=True, help_text=_('When was the goal last updated'))
    
    
    class Meta:
        verbose_name = _('goal')
        verbose_name_plural = _('goals')
        
    
    def get_absolute_url(self):
        return "http://%s/admin/goals/goal/%d/" % (get_domain(), self.id)
    
    
    def __unicode__(self):
        return self.name