from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from ecclesia.discussions.models import Discussion, Story
from ecclesia.groups.models import GroupProfile

class Voting(models.Model):
    discussion = models.ForeignKey(Discussion, verbose_name=_('discussion'), related_name='votings', help_text=_('The discussion that is being voted.'))
    votes_per_participant = models.PositiveIntegerField(_('votes per participant'), default=1)
    status = models.CharField(max_length=50, choices = (('Started', 'Started'), ('Ended', 'Ended')))
    start_time = models.DateTimeField(_('start time'), auto_now_add=True) 
    end_time = models.DateTimeField(_('end time'), null=True, blank=True)
    percent_voted = models.PositiveIntegerField(_('percent voted'), default=0)
    created_by = models.ForeignKey(User, verbose_name=_('created by'), help_text=_('The user that started the voting.'))
    decisions_list = models.TextField(_('decisions_list'), null=True, blank=True, editable=False)

    class Meta:
        ordering = ['-end_time']

    __unicode__ = lambda self: u'Vote on %s' % self.discussion

    def get_voting_group(self):
        return GroupProfile.objects.get(group=self.discussion.group)


class Decision(models.Model):
    discussion = models.ForeignKey(Discussion, verbose_name=_('discussion'), related_name='decisions', help_text=_("The discussion this decision relates to."), null=True)
    voting = models.ForeignKey(Voting, verbose_name=_('voting'), related_name='decisions', help_text=_('The vote in which this decision has been made in.'), null=True)
    decision_story = models.ForeignKey(Story, verbose_name=_('decision story'), related_name='decisions', help_text=_('The story that has been chosen after voting.'))
    percent_of_ballots = models.PositiveIntegerField(null=True, blank=True)
    
    __unicode__ = lambda self: self.decision_story


class BallotManager(models.Manager):
    def _get_voting(self, args):
        voting = None
        if args.has_key('voting'):
            voting = args['voting']
        elif args.has_key('discussion'):
            voting = args['discussion'].votings.filter(status='Started').order_by('-start_time')
            if voting:
                voting = voting[0]
        return voting

    def count_left(self, **kwargs):
        voting = self._get_voting(kwargs)
        if not voting:
            return 0
        return self.filter(user=kwargs['user'], voting=voting, status="Not used").count()

    def used(self, **kwargs):
        voting = self._get_voting(kwargs)
        if not voting:
            return 0
        return self.filter(user=kwargs['user'], voting=voting, status="Used")

class Ballot(models.Model):
    user = models.ForeignKey(User, verbose_name=_('created by'), help_text=_('The user that has the ballot.'))
    story = models.ForeignKey(Story, verbose_name=_('story'), null=True, blank=True, related_name='ballots', help_text=_('The story that have the ballot.'))
    voting = models.ForeignKey(Voting, verbose_name=_('voting'), related_name='ballots', help_text=_('The voting that ballot belongs to.'))
    status = models.CharField(max_length=50, choices = (('Used', 'Used'), ('Not used', 'Not used')))

    objects = BallotManager()

    __unicode__ = lambda self: u"%s's ballot on %s in %s" % (self.user, self.story, self.voting)


def discussion_has_voting(discussion):
    return Voting.objects.filter(discussion=discussion, status='Started')