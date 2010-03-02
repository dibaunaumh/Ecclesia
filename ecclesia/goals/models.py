from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from common.utils import get_domain
from groups.models import GroupProfile
from django.contrib.contenttypes import generic
from discussions.models import Story


class Goal(models.Model):
    """
    An agreed goal of a group.
    """
    group_profile = models.ForeignKey(GroupProfile, verbose_name=_('group profile'), related_name='goals', help_text=_("The goal's group"))
    name = models.SlugField(_('name'), help_text=_('The name of the goal. No whitespaces allowed - use hyphen to separate words.'))
    short_description = models.CharField(_('short description'), max_length=500, help_text=_('A short description of the goal.'))
    parent = models.ForeignKey('self', verbose_name=_('parent'), related_name='children', null=True, blank=True, help_text=_('The parent goal containing this goal'))
    forked_from = models.ForeignKey('self', verbose_name=_('forked from'), related_name='forks', null=True, blank=True, help_text=_('The goal from which this goal forked'))
    #tags
    created_by = models.ForeignKey(User, verbose_name=_('created by'), null=True, blank=True, help_text=_('The user that created the goal'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, help_text=_('When was the goal created'))
    updated_at = models.DateTimeField(_('updated at'), auto_now=True, help_text=_('When was the goal last updated'))
    
    stories = generic.GenericRelation(Story, verbose_name=_('stories'))
    
    class Meta:
        verbose_name = _('goal')
        verbose_name_plural = _('goals')
        
    
    def get_absolute_url(self):
        return "http://%s/goal/%d/visualize" % (get_domain(), self.id)
    
    
    def __unicode__(self):
        return self.name
    
class CourseOfAction(models.Model):
    """
    A  proposed course of action
    """
    goal = models.ForeignKey(Goal, verbose_name=_('goal'), help_text=_("The course of action's goal"))
    name = models.SlugField(_('name'), help_text=_('The name of the course of action. No whitespaces allowed - use hyphen to separate words.'))
    short_description = models.CharField(_('short description'), max_length=500, help_text=_('A short description of the goal.'))
    parent = models.ForeignKey('self', verbose_name=_('parent'), related_name='children', null=True, blank=True, help_text=_('The parent goal containing this goal'))
    forked_from = models.ForeignKey('self', verbose_name=_('forked from'), related_name='forks', null=True, blank=True, help_text=_('The goal from which this goal forked'))
    possible_results = models.ManyToManyField('PossibleResult', verbose_name=_('possible results'), related_name='courses_of_action', through='CausingRelation', blank=True, null=True)
    #tags
    created_by = models.ForeignKey(User, verbose_name=_('created by'), null=True, blank=True, help_text=_('The user that created the goal'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, help_text=_('When was the goal created'))
    updated_at = models.DateTimeField(_('updated at'), auto_now=True, help_text=_('When was the goal last updated'))
    
    class Meta:
        verbose_name = _('course of action')
        verbose_name_plural = _('courses of action')
    
    def get_absolute_url(self):
        return "http://%s/admin/goals/courseofaction/%s/" % (get_domain(), self.name)

    def __unicode__(self):
        return self.name        

class PossibleResult(models.Model):
    """
    A possible result of a course of action
    """
    goal = models.ForeignKey(Goal, verbose_name=_('goal'), help_text=_("The course of action's goal"))
    name = models.SlugField(_('name'), help_text=_('The name of the course of action. No whitespaces allowed - use hyphen to separate words.'))
    short_description = models.CharField(_('short description'), max_length=500, help_text=_('A short description of the goal.'))
    parent = models.ForeignKey('self', verbose_name=_('parent'), related_name='children', null=True, blank=True, help_text=_('The parent goal containing this goal'))
    forked_from = models.ForeignKey('self', verbose_name=_('forked from'), related_name='forks', null=True, blank=True, help_text=_('The goal from which this goal forked'))
    goals = models.ManyToManyField(Goal, verbose_name=_('goals'), related_name='possible_results', through='LeadingRelation')
    #tags
    created_by = models.ForeignKey(User, verbose_name=_('created by'), null=True, blank=True, help_text=_('The user that created the goal'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, help_text=_('When was the goal created'))
    updated_at = models.DateTimeField(_('updated at'), auto_now=True, help_text=_('When was the goal last updated'))
    
    class Meta:
        verbose_name = _('possible result')
        verbose_name_plural = _('possible result')
    
    def get_absolute_url(self):
        return "http://%s/admin/goals/possibleresult/%s/" % (get_domain(), self.name)

    def __unicode__(self):
        return self.name       
    
class CausingRelation(models.Model):
    """
    A causal relation between course of action and possible result
    """
    course_of_action       = models.ForeignKey('CourseOfAction', verbose_name=_('course of action'))
    possible_result        = models.ForeignKey('PossibleResult', verbose_name=_('possible result'))
    #tags
    created_by = models.ForeignKey(User, verbose_name=_('created by'), null=True, blank=True, help_text=_('The user that created the goal'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, help_text=_('When was the goal created'))
    updated_at = models.DateTimeField(_('updated at'), auto_now=True, help_text=_('When was the goal last updated'))

    def get_absolute_url(self):
        return "http://%s/admin/goals/causingrelation/%s/" % (get_domain(), self.name)

    def __unicode__(self):
        return "%s:%s"%(self.course_of_action.name, self.possible_result.name)   

    class Meta:
        verbose_name = _('causing relation')
        verbose_name_plural = _('causing relations')
          
class LeadingRelation(models.Model):
    """
    A relation between a possible result and a goal that it leads to
    """
    possible_result        = models.ForeignKey('PossibleResult', verbose_name=_('possible result'))
    goal                   = models.ForeignKey('Goal', verbose_name=_('goal'))
    #tags
    created_by = models.ForeignKey(User, verbose_name=_('created by'), null=True, blank=True, help_text=_('The user that created the goal'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, help_text=_('When was the goal created'))
    updated_at = models.DateTimeField(_('updated at'), auto_now=True, help_text=_('When was the goal last updated'))

    def get_absolute_url(self):
        return "http://%s/admin/goals/leadingrelation/%s/" % (get_domain(), self.name)

    def __unicode__(self):
        return "%s:%s"%(self.possible_result.name, self.goal.name)   

    class Meta:
        verbose_name = _('leading relation')
        verbose_name_plural = _('leading relations')
    
