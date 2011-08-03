from django.contrib.auth.forms import SetPasswordForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from common.send_mail import send_mail
from django.contrib.sites.models import get_current_site
from groups.models import LostPassword
from models import *
from ecclesia.discussions.models import Story, Discussion
from ecclesia.groups.models import GroupProfile
import datetime
import settings

@csrf_exempt
def update_presentation(request):
    """
    Update the presentation feilds of elements on the featured view
    """
    model_name = request.POST.get('model_name', None)
    update_time = False
    timestamp = datetime.datetime.now()
    if model_name:
        model_class = globals()[model_name]
        pk = request.POST.get('pk', None)
        if pk:
            object = model_class.objects.get(pk=pk)
            if hasattr(object, 'get_visual_container'):
                container = object.get_visual_container()
                if object and hasattr(container, 'last_related_update'):
                    last_changed = request.POST.get('last_changed', None)
                    if last_changed:
                        try:
                            last_changed_datetime = datetime.datetime.strptime(last_changed, '%Y-%m-%d %H:%M:%S.%f')
                        except:
                            last_changed_datetime = datetime.datetime.strptime(last_changed, '%Y-%m-%d %H:%M:%S')
                        if last_changed_datetime < container.last_related_update:
                            timestamp = last_changed
                        else:
                            update_time = True
            object.x = int(request.POST.get('x', object.x))
            object.y = int(request.POST.get('y', object.y))
            object.save()
            print "Coordinates updated successfully."
        else:
            print "Object's pk not specified."
    else:
        print "Model name not specified."
    if update_time:
        timestamp = object.updated_at if hasattr(object, 'updated_at') else timestamp
    return HttpResponse(str(timestamp))

def presentation_status(request, model_name, object_pk):
    datetime_format = '%Y-%m-%d %H:%M:%S.%f'
    last_changed_client = request.POST.get('last_changed', None)
    last_changed_db = ''
    try:
        model_class = globals()[model_name]
    except:
        return Http404()
    if model_class:
        object = model_class.objects.get(pk=object_pk)
        if object and hasattr(object, 'last_related_update'):
            last_changed_db = object.last_related_update
    if not last_changed_client:
        return HttpResponse(str(last_changed_db))
    else:
        try:
            last_changed_client = datetime.datetime.strptime(last_changed_client, datetime_format)
            if last_changed_client < last_changed_db:
                last_changed_client = last_changed_db
            return HttpResponse(str(last_changed_client))
        except: # probably the last_changed value isn't in the right format
            return HttpResponse(str(last_changed_db))

def _follow(user, followed_object):
    if user and followed_object:
        subscription = Subscription()
        subscription.user = user
        subscription.followed_object = followed_object
        subscription.save()
        return HttpResponse('success')
    else:
        return HttpResponse('error')

def _unfollow(user, followed_object):
    if user and followed_object:
        followed_object_type = ContentType.objects.get_for_model(followed_object)
        subscription = Subscription.objects.filter(user=user, \
            content_type__pk=followed_object_type.id, object_id=followed_object.id)[0]
        subscription.delete()
        return HttpResponse('success')
    else:
        return HttpResponse('error')

def new_key():
    while True:
        key = User.objects.make_random_password(70)
        try:
            LostPassword.objects.get(key=key)
        except LostPassword.DoesNotExist:
            return key

@csrf_protect
def lost_password(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(username=request.POST['username'])
            lostpassword = LostPassword.objects.create(user=user,
                                                       key=new_key())
            message = 'To change your password, click on the following link:\n http://%s%s' % (get_current_site(request),
                reverse('change_password',kwargs={'key':lostpassword.key}))

            send_mail(settings.DEFAULT_FROM_EMAIL, user.email, 'your ekkli password', message)
            return HttpResponseRedirect('/login')
        except User.DoesNotExist:
            message = 'Unknown user'

    else:
        message = ''

    return render_to_response('lost_password.html',
                              {'message': message})


@csrf_protect
def change_password(request, key,
                    template_name='registration/password_change_form.html',
                    post_change_redirect=None,
                    password_change_form=SetPasswordForm,):
    lostpassword = get_object_or_404(LostPassword, key=key)
    if lostpassword.is_expired():
        lostpassword.delete()
        message = 'Page expired'
        context = {
            'form': {},
            'message': message
        }
        return render_to_response(template_name, context)
    else:
        message=''
        if post_change_redirect is None:
            post_change_redirect = reverse('django.contrib.auth.views.password_change_done')


        if request.method == "POST":

            form = password_change_form(user=lostpassword.user, data=request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(post_change_redirect)
            else:
                message = 'You typed two different passwords'

        form = password_change_form(user=request.user)
        context = {
            'form': form,
            'message': message
        }
        return render_to_response(template_name, context)

