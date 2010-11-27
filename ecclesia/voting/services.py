from datetime import timedelta, datetime

from models import *
from forms import *

def get_voting_data(user, voting, discussion):
    time_left_for_voting = 0
    voting_progress_bar_value = calculate_progress_bar_value(voting)
    if voting.end_time:
        time_left_for_voting = str(voting.end_time - datetime.now()).split(".")[0]
        if time_left_for_voting.startswith("-"):
            calculate_decision_of_voting(voting, discussion)
            voting.end_time = datetime.now()
            voting.status = "Ended"
            voting.save()
            return False
    ballots_left = Ballot.objects.count_left(user=user, voting=voting)
    return {
        'voting_progress_bar_value' : voting_progress_bar_value,
        'ballots_left' : ballots_left,
        'voting_time_left' : time_left_for_voting
    }

def calculate_progress_bar_value(voting):
    group = voting.get_voting_group()
    members = group.get_group_members()
    members_that_voted = [member for member in members if not Ballot.objects.count_left(user=member, voting=voting)]
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

def calculate_decision_of_voting(voting, discussion):
    all_ballots = Ballot.objects.filter(voting=voting, status='Used')
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
        best_score = items[0][0]
        if not items[0][1]:
            return False
        for item in items:
            if item[0] == best_score:
                percent_of_ballots = int(items[0][0] / len(all_ballots))
                decision = Decision(discussion=discussion, voting=voting, decision_story=item[1], percent_of_ballots=percent_of_ballots)
                decision.save()
            else:
                break
        return True
    return False