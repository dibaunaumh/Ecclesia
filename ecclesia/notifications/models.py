from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import User, Group
from groups.models import GroupProfile
from discussions.models import Discussion, Story
from django.utils.translation import gettext_lazy as _
from datetime import datetime

class Notification(models.Model):
    """
    Notification that are sent to the User about changes made in discussions
    """
    text = models.TextField(_('text'), max_length=1000, help_text=_("The body text of the notification"))
    recipient = models.ForeignKey(User, verbose_name=_('recipient'), null=True, blank=True, help_text=_('The user that gets the notification'))
    group = models.ForeignKey(Group, default=None, verbose_name=_('group'), help_text=_('The group related to notification'))
    discussion = models.ForeignKey(Discussion, verbose_name=_('discussion'), null=True, blank=True, help_text=_('Discussion that notification talks about'))
    story = models.ForeignKey(Story, verbose_name=_('story'), null=True, blank=True, help_text=_('Story that notification talks about'))
    failed = models.BooleanField(default=False, verbose_name=_('failed'), help_text=_("Boolean field that tells us if we failed to send the notification"))
    fail_reason = models.TextField(_('fail_reason'), max_length=1000, null=True, blank=True, help_text=_("Notification sending failure reason"))
    parent = models.ForeignKey('self', verbose_name=_('parent'), null=True, blank=True, help_text=_('The parent notification containing this notification'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, help_text=_('When was the notification created'))
    updated_at = models.DateTimeField(_('updated at'), auto_now=True, help_text=_('When was the notification last updated'))
    delivered_at = models.DateTimeField(_('delivered at'), null=True, blank=True, help_text=_('When was the notification delivered'))
    read = models.BooleanField(default=False, verbose_name=_('read'), help_text=_("Boolean field that tells us if the notification was read"))
    offline_recipients_only = models.BooleanField(default=False, verbose_name=_('offline recipients only'), 
                                                  help_text=_("Boolean field that tells us if to send the notification to offline recipients only"))
    
    def deliver(self, instance):
        if instance.recipient and instance.recipient.email:
            try:
                send_mail('Email from ekkli', instance.text, 'ekkli@gmail.com',
                          [instance.recipient.email], fail_silently=False)
                instance.delivered_at = datetime.now()
                instance.save()
            except Exception as inst:
                instance.delivered_at = None
                instance.failed = True
                instance.fail_reason = inst
                instance.save()
                print inst
        elif not instance.recipient:
            group = instance.group
            members = GroupProfile.objects.filter(group=group)[0].get_group_members()
            for member in members:
                notification = Notification(text=instance.text, group=instance.group, recipient=member)
                notification.save()
        else:
            pass

def send_notification(sender, instance, **kwargs):
    if instance.delivered_at is None:
        instance.deliver(instance)
            
# connecting post_save signal of Notifications to the function that sends emails 
models.signals.post_save.connect(send_notification, sender=Notification)