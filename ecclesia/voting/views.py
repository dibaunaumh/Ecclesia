from datetime import datetime
from django.http import HttpResponse, Http404, HttpResponseServerError
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from ecclesia.discussions.models import Discussion, Story
from models import Voting, Ballot
from ecclesia.voting.forms import VotingForm
from ecclesia.voting.services import add_ballots_to_members, save_voting_data, calculate_decision_of_voting
from django.contrib.auth.decorators import login_required


def end_voting(request):
    response = ''
    if 'discussion_id' in request.POST and request.POST['discussion_id']:
        discussion = Discussion.objects.get(id=request.POST['discussion_id'])
        voting=Voting.objects.filter(discussion=discussion, status='Started')[0]
        has_decision = calculate_decision_of_voting(voting, discussion)
        voting.end_time = datetime.now()
        voting.status = "Ended"
        voting.save()
        response = 'SUCCESS'
    return HttpResponse(response)

@login_required
def add_ballot(request, discussion_pk):
    if request.POST:
        story_pk = request.POST.get('story_pk', None)
        if not story_pk:
            return HttpResponseServerError(_('No story id found in request.'))
        discussion = Discussion.objects.get(pk=discussion_pk)
        story = Story.objects.get(pk=story_pk)
        voting = Voting.objects.filter(discussion=discussion, status='Started')[0]
        ballot = Ballot.objects.filter(user=request.user,voting=voting,status='Not used')
        if ballot:
            ballot = ballot[0]
        else:
            return HttpResponseServerError(_("Seems like you've used up all your ballots for this vote."))
        ballot.status = 'Used'
        ballot.story = story
        ballot.save()
    else:
        return HttpResponseServerError(_('Bad usage. No post params present in request.'))
    return HttpResponse('SUCCESS')

@login_required
def remove_ballot(request, discussion_pk):
    if request.POST:
        story_pk = request.POST.get('story_pk', None)
        if not story_pk:
            return HttpResponseServerError(_('No story id found in request.'))
        discussion = Discussion.objects.get(pk=discussion_pk)
        story = Story.objects.get(pk=story_pk)
        voting = Voting.objects.filter(discussion=discussion, status='Started')[0]
        ballot = Ballot.objects.filter(user=request.user,voting=voting,story=story,status='Used')[0]
        ballot.status = 'Not used'
        ballot.story = None
        ballot.save()
    else:
        return HttpResponseServerError(_('Bad usage. No post params present in request.'))
    return HttpResponse("SUCCESS")

@login_required
def get_voting_form(request):
    voting_form = VotingForm()
    return HttpResponse(voting_form.as_p())

@login_required
def start_voting(request, discussion_pk):
    if request.POST and discussion_pk:
        discussion = Discussion.objects.get(id=discussion_pk)
        voting_form = VotingForm(request.POST)
        if voting_form.is_valid():
            voting = save_voting_data(request.user, discussion, voting_form.cleaned_data)
            add_ballots_to_members(voting)
        else:
            return  HttpResponseServerError(voting_form.as_p())
    return HttpResponse('{"ballots":%d,"time_left":"%s"}' % (voting_form.cleaned_data['votes_per_participant'], 'Two weeks'))