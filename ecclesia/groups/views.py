from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from groups.models import *



def home(request):
    """Renders the application home page"""
    groups = GroupProfile.objects.all()
    return render_to_response('home.html', locals())
