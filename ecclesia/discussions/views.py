from ecclesia.discussions.models import Story
from ecclesia.discussions.forms import StoryForm
from django.shortcuts import render_to_response
from django.http import HttpResponse

def submit_story(request):
    story = Story(created_by=request.user)
    form = StoryForm(request.POST, instance=story)
    try:
        form.save()
    except ValueError:
        return render_to_response('write_story_miniform.html', {'form':form})
    return HttpResponse('OK')
