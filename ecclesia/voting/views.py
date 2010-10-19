from datetime import datetime
from django.http import HttpResponse

from discussions.models import Discussion 
from models import Voting

def end_voting(request):
    if 'discussion_id' in request.POST and request.POST['discussion_id']:
        discussion = Discussion.objects.get(id=request.POST['discussion_id'])
        voting=Voting.objects.filter(discussion=discussion, status='Started')[0]
        voting.end_time = datetime.now()
        voting.status = "Ended"
        voting.save()
    return HttpResponse("SUCCESS")
    