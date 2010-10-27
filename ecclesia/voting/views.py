from datetime import datetime
from django.http import HttpResponse

from discussions.models import Discussion, Story
from models import Voting, Ballot

def end_voting(request):
    if 'discussion_id' in request.POST and request.POST['discussion_id']:
        discussion = Discussion.objects.get(id=request.POST['discussion_id'])
        voting=Voting.objects.filter(discussion=discussion, status='Started')[0]
        voting.end_time = datetime.now()
        voting.status = "Ended"
        voting.save()
    return HttpResponse("SUCCESS")

def add_ballot(request, discussion_pk, story_pk):
    discussion = Discussion.objects.get(pk=discussion_pk)
    story = Story.objects.get(pk=story_pk)
    voting = Voting.objects.filter(discussion=discussion, status='Started')[0]
    ballot = Ballot.objects.filter(user=request.user,voting=voting,status='Not used')[0]
    ballot.status = 'Used'
    ballot.story = story
    ballot.save()
    return HttpResponse("SUCCESS")
    
def remove_ballot(request, discussion_pk, story_pk):
    discussion = Discussion.objects.get(pk=discussion_pk)
    story = Story.objects.get(pk=story_pk)
    voting = Voting.objects.filter(discussion=discussion, status='Started')[0]
    ballot = Ballot.objects.filter(user=request.user,voting=voting,story=story,status='Used')[0]
    ballot.status = 'not used'
    ballot.story = None
    ballot.save()
    return HttpResponse("SUCCESS")
    