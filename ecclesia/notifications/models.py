from datetime import datetime

from django.db import models
#from django.core.mail import send_mail
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from groups.models import GroupProfile
from discussions.models import Discussion, Story
from common.models import Subscription
from common.send_mail import send_mail


class Notification(models.Model):
    """
    Notification that are sent to the User about changes made in discussions
    """
    text = models.TextField(_('text'), max_length=1000, help_text=_("The body text of the notification"))
    recipient = models.ForeignKey(User, related_name='recipient', verbose_name=_('recipient'), null=True, blank=True, help_text=_('The user that gets the notification'))
    acting_user = models.ForeignKey(User, related_name='acting_user', verbose_name=_('acting_user'), null=True, blank=True, help_text=_('The user who made the change that caused the notification'))
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    entity = generic.GenericForeignKey('content_type', 'object_id')
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
                send_mail('alexarsh5@gmail.com', instance.recipient.email, 
                          'Email from ekkli', instance.text)
                instance.delivered_at = datetime.now()
                instance.save()
            except Exception as inst:
                instance.delivered_at = None
                instance.failed = True
                instance.fail_reason = inst
                instance.save()
                print inst
        elif not instance.recipient:
            group = instance.entity.discussion.group
            members = GroupProfile.objects.filter(group=group)[0].get_group_members()
            for member in members:
                for s in Subscription.objects.all():
                    if s.user == member and s.followed_object == instance.entity.discussion \
                    and instance.acting_user != member:
                        notification = Notification(text=instance.text, entity=instance.entity, recipient=member)
                        notification.save()
        else:
            return

def send_notification(sender, instance, **kwargs):
    if instance.delivered_at is None:
        if instance.entity and instance.entity.discussion and \
            instance.text.find("To go to discussion click on the following link") == -1: 
            instance.text = "%s\nTo go to discussion click on the following link: %s" % \
            (instance.text, instance.entity.discussion.get_absolute_url())
        instance.deliver(instance)
            
# connecting post_save signal of Notifications to the function that sends emails 
models.signals.post_init.connect(send_notification, sender=Notification)