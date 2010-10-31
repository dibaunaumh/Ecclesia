import datetime
from datetime import timedelta

from models import *
from forms import *
from groups.models import Group, GroupProfile

def handle_voting(request, discussion, has_voting):
    errors_in_voting_form = ''
    voting_form = VotingForm()
    voting_progress_bar_value = 0
    ballots = 0
    stories_with_votes = {}
    time_left_for_voting = 0
    group = GroupProfile.objects.get(group=Group.objects.get(id=discussion.group.pk))
    if request.POST:
        voting_form = VotingForm(request.POST)
        if voting_form.is_valid():
            voting = save_voting_data(request.user, discussion, voting_form.cleaned_data)
            add_ballots_to_members(group, voting)
        else:
            errors_in_voting_form = True
    if has_voting:
        voting_progress_bar_value = calculate_progress_bar_value(discussion)
        voting = Voting.objects.filter(discussion=discussion, status='Started')[0]
        if voting.end_time:
            time_left_for_voting = str(voting.end_time - datetime.now()).split(".")[0]
            if time_left_for_voting.startswith("-"):
                voting.end_time = datetime.now()
                voting.status = "Ended"
                voting.save()
                has_voting = discussion_has_voting(discussion)
        if str(request.user) != 'AnonymousUser':
            ballots = len(Ballot.objects.filter(user=request.user, voting=voting, status="Not used"))
            used_ballots = Ballot.objects.filter(user=request.user, voting=voting, status="Used")
            if used_ballots:
                for ballot in used_ballots:
                    if ballot.story.pk in stories_with_votes.keys():
                        stories_with_votes[ballot.story.pk] = stories_with_votes[ballot.story.pk] + 1
                    else:
                        stories_with_votes[ballot.story.pk] = 1
    return (voting_form, errors_in_voting_form, voting_progress_bar_value, \
     ballots, stories_with_votes, time_left_for_voting)
    
def calculate_progress_bar_value(discussion):
    voting = Voting.objects.filter(discussion=discussion, status='Started')[0]
    group = GroupProfile.objects.get(group=Group.objects.get(id=discussion.group.pk))
    members = group.get_group_members()
    members_that_voted = [member for member in members if not Ballot.objects.filter(user=member, voting=voting, status="Not used")]
    return len(members_that_voted) / len(members) * 100 
    
def add_ballots_to_members(group, voting):
    members = group.get_group_members()
    for member in members:
        for vote in range(voting.votes_per_participant):
            Ballot(user=member, voting=voting, status="Not used").save()
    
def save_voting_data(user, discussion, voting_data):
    voting = Voting(discussion=discussion, created_by=user)
    voting.votes_per_participant = voting_data['votes_per_participant']
    voting.status = 'Started'
    minutes = 0
    if voting_data['days']:
        minutes += voting_data['days'] * 24 * 60
    if voting_data['hours']:
        minutes += voting_data['hours'] * 60
    if voting_data['minutes']:
        minutes += voting_data['minutes']
    voting.save()
    duration = timedelta(minutes=minutes) 
    voting.end_time = voting.start_time + duration
    voting.save()
    return voting