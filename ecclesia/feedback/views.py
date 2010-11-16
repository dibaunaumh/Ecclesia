import datetime
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect

from models import Feedback
from forms import FeedbackForm

@csrf_protect
def index(request, form_class=FeedbackForm, 
          template_name='feedback/feedback_form.html',
          success_template_name='feedback/feedback_thanks.html',
          success_url='/feedback/thanks/',
          extra_context=None):

    if request.method == "POST":
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            feedback = form.save()
            if isinstance(request.user, User):
                feedback.user = request.user
            if 'HTTP_USER_AGENT' in request.META:
                feedback.browser = request.META['HTTP_USER_AGENT']
            feedback.save()
            if request.is_ajax():
                return render_to_response(success_template_name)
                
            redirect(success_url)
    else:
        form = form_class()

    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    return render_to_response(template_name,
                              {'form': form},
                              context_instance=context)

