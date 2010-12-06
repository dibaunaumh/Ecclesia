from datetime import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from ecclesia.discussions.models import Discussion, Story
from ecclesia.groups.models import GroupProfile
#from ecclesia.voting.services import calculate_decisions_of_voting


class VotingManager(models.Manager):
    def get_started(self, **kwargs):
        if kwargs.has_key('discussion'):
            try:
                return self.filter(discussion=kwargs['discussion'], status='Started').order_by('-start_time')[0]
            except:
                return None
        else:
            return None

class Voting(models.Model):
    discussion = models.ForeignKey(Discussion, verbose_name=_('discussion'), related_name='votings', help_text=_('The discussion that is being voted.'))
    votes_per_participant = models.PositiveIntegerField(_('votes per participant'), default=1)
    status = models.CharField(max_length=50, choices = (('Started', 'Started'), ('Ended', 'Ended')), default='Started')
    start_time = models.DateTimeField(_('start time'), auto_now_add=True) 
    end_time = models.DateTimeField(_('end time'), null=True, blank=True)
    percent_voted = models.PositiveIntegerField(_('percent voted'), default=0)
    created_by = models.ForeignKey(User, verbose_name=_('created by'), help_text=_('The user that started the voting.'))
    decisions_list = models.TextField(_('decisions_list'), null=True, blank=True, editable=False)

    class Meta:
        verbose_name = _('vote process')
        verbose_name_plural = _('vote processes')
        ordering = ['-end_time']

    objects = VotingManager()

    __unicode__ = lambda self: u'Vote on %s' % self.discussion

    def get_voting_group(self):
        return GroupProfile.objects.get(group=self.discussion.group)

    def time_left(self):
        delta = self.end_time - datetime.now()
#        return str(delta).split('.')[0] if delta.total_seconds() > 0 else 0 # timedelta.total_seconds() is new from python 2.7
        total_seconds = lambda td: (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6
        return str(delta).split('.')[0] if total_seconds(delta) > 0 else 0

    def close(self, discussion=None):
        self.status = 'Ended'
        now = datetime.now()
        if now > self.end_time:
            self.end_time = now
        self.save()


class Decision(models.Model):
    discussion = models.ForeignKey(Discussion, verbose_name=_('discussion'), related_name='decisions', help_text=_("The discussion this decision relates to."), null=True)
    voting = models.ForeignKey(Voting, verbose_name=_('voting'), related_name='decisions', help_text=_('The vote in which this decision has been made in.'), null=True)
    decision_story = models.ForeignKey(Story, verbose_name=_('decision story'), related_name='decisions', help_text=_('The story that has been chosen after voting.'))
    percent_of_ballots = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = _('decision')
        verbose_name_plural = _('decisions')

    __unicode__ = lambda self: self.decision_story.__unicode__()


class BallotManager(models.Manager):
    def _get_voting(self, args):
        voting = None
        if args.has_key('voting'):
            voting = args['voting']
        elif args.has_key('discussion'):
            voting = Voting.objects.get_started(discussion=args['discussion'])
        return voting

    def count_left(self, **kwargs):
        voting = self._get_voting(kwargs)
        if not voting:
            return 0
        return voting.votes_per_participant - self.filter(user=kwargs['user'], voting=voting).count()

    def used(self, **kwargs):
        voting = self._get_voting(kwargs)
        if not voting:
            return 0
        return self.filter(user=kwargs['user'], voting=voting)

class Ballot(models.Model):
    user = models.ForeignKey(User, verbose_name=_('created by'), help_text=_('The user that has the ballot.'))
    story = models.ForeignKey(Story, verbose_name=_('story'), null=True, blank=True, related_name='ballots', help_text=_('The story that have the ballot.'))
    voting = models.ForeignKey(Voting, verbose_name=_('voting'), related_name='ballots', help_text=_('The voting that ballot belongs to.'))
#    status = models.CharField(max_length=50, choices = (('Used', 'Used'), ('Not used', 'Not used')))

    class Meta:
        verbose_name = _('ballot')
        verbose_name_plural = _('ballots')

    objects = BallotManager()

    __unicode__ = lambda self: u"%s's ballot on %s in %s" % (self.user, self.story, self.voting)