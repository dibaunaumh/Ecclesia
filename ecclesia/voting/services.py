from datetime import timedelta
from models import *
from forms import *

def get_voting_data(user, voting, discussion):
    voting_progress_bar_value = calculate_progress_bar_value(voting)
    time_left_for_voting = voting.time_left()
    if not time_left_for_voting:
        close_voting(voting, discussion)
        return False
    ballots_left = Ballot.objects.count_left(user=user, voting=voting)
    return {
        'voting_progress_bar_value' : voting_progress_bar_value,
        'ballots_left' : ballots_left,
        'voting_time_left' : time_left_for_voting
    }

def close_voting(voting, discussion):
    voting.close(discussion)
    clean_old_decisions(discussion)
    calculate_voting_decisions(voting, discussion)

def calculate_progress_bar_value(voting):
    group = voting.get_voting_group()
    members = group.get_group_members()
    members_that_voted = [member for member in members if not Ballot.objects.count_left(user=member, voting=voting)]
    return float(len(members_that_voted)) / float(len(members)) * 100

def calculate_voting_time_left(voting_data):
    minutes = 0
    if voting_data['days']:
        minutes += voting_data['days'] * 24 * 60
    if voting_data['hours']:
        minutes += voting_data['hours'] * 60
    if voting_data['minutes']:
        minutes += voting_data['minutes']
    return minutes

def open_voting_from_data(user, discussion, voting_data):
    voting = Voting(discussion=discussion, created_by=user)
    voting.votes_per_participant = voting_data['votes_per_participant']
    minutes = calculate_voting_time_left(voting_data)
    duration = timedelta(minutes=minutes)
    #TODO: saving here the instance twice, just to get the start_time that has auto_now_add=True
    voting.save() # save first so we have the initial start_time
    voting.end_time = voting.start_time + duration
    voting.save()
    return voting

def clean_old_decisions(discussion):
    if discussion.decisions:
        discussion.decisions.clear()

def calculate_voting_decisions(voting, discussion):
    all_ballots = Ballot.objects.select_related().filter(voting=voting)
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
        percent_of_ballots = int(items[0][0] / len(all_ballots))
        for item in items:
            if item[0] == best_score:
                Decision.objects.create(discussion=discussion, voting=voting, decision_story=item[1], percent_of_ballots=percent_of_ballots)
            else:
                break
        return True
    return False