from datetime import timedelta

from models import *
from forms import *
from ecclesia.discussions.models import Discussion

def handle_voting(request, discussion_pk):
    voting_progress_bar_value = 0
    ballots = 0
    stories_with_votes = {}
    time_left_for_voting = 0
    discussion = Discussion.objects.get(id=discussion_pk)
    if discussion_has_voting(discussion):
        voting = Voting.objects.filter(discussion=discussion, status='Started')[0]
        voting_progress_bar_value = calculate_progress_bar_value(voting)
        if voting.end_time:
            time_left_for_voting = str(voting.end_time - datetime.now()).split(".")[0]
            if time_left_for_voting.startswith("-"):
                calculate_decision_of_voting(voting)
                voting.end_time = datetime.now()
                voting.status = "Ended"
                voting.save()
        if request.user.is_authenticated():
            ballots = len(Ballot.objects.filter(user=request.user, voting=voting, status="Not used"))
            used_ballots = Ballot.objects.filter(user=request.user, voting=voting, status="Used")
            if used_ballots:
                for ballot in used_ballots:
                    if ballot.story.pk in stories_with_votes.keys():
                        stories_with_votes[ballot.story.pk] = stories_with_votes[ballot.story.pk] + 1
                    else:
                        stories_with_votes[ballot.story.pk] = 1
    return {
        'stories_with_votes' : stories_with_votes,
        'voting_progress_bar_value' : voting_progress_bar_value,
        'voting_ballots' : ballots,
        'voting_time_left' : time_left_for_voting
    }

def calculate_progress_bar_value(voting):
    group = voting.get_voting_group()
    members = group.get_group_members()
    members_that_voted = [member for member in members if not Ballot.objects.filter(user=member, voting=voting, status="Not used")]
    return len(members_that_voted) / len(members) * 100 
    
def add_ballots_to_members(voting):
    group = voting.get_voting_group()
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

def calculate_decision_of_voting(voting):
    all_ballots = Ballot.objects.filter(voting=voting)
    if all_ballots:
        results = {}
        for ballot in all_ballots:
            if not ballot.story in results:
                results[ballot.story] = 1
            else:
                results[ballot.story] += 1
        items = [(v, k) for k, v in results.items()]
        items.sort()
        items.reverse()
        voting.decision_story = items[0][1]
        voting.save()
        percent_of_ballots = int(items[0][0] / len(all_ballots))
        if not Decision.objects.filter(voting=voting): 
            decision = Decision(voting=voting, discussion=voting.discussion, \
                     decision_story = items[0][1], percent_of_ballots=percent_of_ballots)
        else:
            decision = Decision.objects.filter(voting=voting)[0]
            decision.decision_story = items[0][1]
            decision.percent_of_ballots=percent_of_ballots
        decision.save()
    
    
    
    