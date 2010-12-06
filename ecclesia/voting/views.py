from datetime import datetime
from django.http import HttpResponse, HttpResponseServerError
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from ecclesia.discussions.models import Discussion, Story
from models import Voting, Ballot
from ecclesia.voting.forms import VotingForm
from ecclesia.voting.services import open_voting_from_data, calculate_progress_bar_value, close_voting


@login_required
def end_voting(request):
    if 'discussion_id' in request.POST and request.POST['discussion_id']:
        discussion = Discussion.objects.get(id=request.POST['discussion_id'])
        voting = Voting.objects.get_started(discussion=discussion)
        if not voting:
            return HttpResponseServerError(_('{"VOTE_ENDED":"Sorry, probably the vote has ended."}'))
        close_voting(voting, discussion)
    return HttpResponse('SUCCESS')

@login_required
def add_ballot(request):
    if request.POST:
        story_pk = request.POST.get('story_pk', None)
        if not story_pk:
            return HttpResponseServerError(_('No story id found in request.'))
        story = Story.objects.get(pk=story_pk)
        discussion = story.discussion
        voting = Voting.objects.get_started(discussion=discussion)
        if not voting:
            return HttpResponseServerError(_('{"VOTE_ENDED":"Sorry, probably the vote has ended."}'))
        if voting.time_left():
            user = request.user
            if Ballot.objects.count_left(user=user, voting=voting):
                Ballot.objects.create(user=user, voting=voting, story=story)
            else:
                return HttpResponseServerError(_('{"NO_BALLOT":"Seems like you\'ve used up all your ballots for this vote."}'))
        else:
            close_voting(voting, discussion)
            return HttpResponseServerError(_('{"VOTE_ENDED":"Oops, looks like your time is up."}'))
    else:
        return HttpResponseServerError(_('Bad usage. No post params present in request.'))
    return HttpResponse('SUCCESS')

@login_required
def remove_ballot(request):
    if request.POST:
        story_pk = request.POST.get('story_pk', None)
        if not story_pk:
            return HttpResponseServerError(_('No story id found in request.'))
        story = Story.objects.get(pk=story_pk)
        discussion = story.discussion
        voting = Voting.objects.get_started(discussion=discussion)
        if not voting:
            return HttpResponseServerError(_('{"VOTE_ENDED":"Sorry, probably the vote has ended."}'))
        if voting.time_left():
            ballots = Ballot.objects.filter(user=request.user,voting=voting,story=story)
            if ballots:
                ballot = ballots[0]
            else:
                return HttpResponseServerError(_('{"NO_BALLOT":"Funnybone, You haven\'t voted on this story yet."}'))
            ballot.delete()
        else:
            close_voting(voting, discussion)
            return HttpResponseServerError(_('{"VOTE_ENDED":"Oops, looks like your time is up."}'))
    else:
        return HttpResponseServerError(_('Bad usage. No post params present in request.'))
    return HttpResponse("SUCCESS")

@login_required
def get_voting_form(request, discussion_pk):
    # check if there's a vote in progress
    if Voting.objects.get_started(discussion=discussion_pk):
        return HttpResponseServerError(_('{"VOTE_STARTED":"Hold it, there is a vote in progress."}'))
    voting_form = VotingForm()
    return HttpResponse(voting_form.as_p())

@login_required
def start_voting(request, discussion_pk):
    if request.POST and discussion_pk:
        discussion = Discussion.objects.get(id=discussion_pk)
        # check if there's a vote in progress
        if Voting.objects.get_started(discussion=discussion):
            return HttpResponseServerError(_("Hold it, there is a vote in progress."))
        voting_form = VotingForm(request.POST)
        if voting_form.is_valid():
            voting = open_voting_from_data(request.user, discussion, voting_form.cleaned_data)
        else:
            return  HttpResponseServerError(voting_form.as_p())
        return HttpResponse('{"ballots":%d,"time_left":"%s"}' % (voting.votes_per_participant, voting.end_time - voting.start_time))
    else:
        return HttpResponseServerError(_("Bad usage. Need post params with a discussion's pk."))

@login_required
def get_vote_progress(request, discussion_pk):
    voting = Voting.objects.select_related().filter(discussion=discussion_pk, status='Started')
    if voting:
        voting = voting[0]
        if voting.time_left():
            progress = calculate_progress_bar_value(voting)
            time_left = voting.end_time - datetime.now()
            return HttpResponse('{"progress":%d,"time_left":"%s"}' % (progress, time_left))
        else:
            close_voting(voting, voting.discussion)
            return HttpResponseServerError(_('{"VOTE_ENDED":"Oops, looks like your time is up."}'))
    else:
        return HttpResponseServerError(_('{"VOTE_ENDED":"Sorry, probably the vote has ended."}'))