from django.test import TestCase
from django.core import mail
from django.contrib.auth.models import Group, User
from models import Notification
from ecclesia.groups.models import GroupProfile
from ecclesia.discussions.models import Discussion, DiscussionType

class NotificationsTest(TestCase):
    
    def setUp(self):
        discussion_type = DiscussionType(name="test_discussion_type")
        discussion_type.save()
        group = Group(name="test_group")
        group.save()
        user = User(username="test_user", password="test_password", email="test@email.com")
        user.save()
        user2 = User(username="test_user2", password="test_password2", email="test@email.com")
        user2.save()
        group_profile = GroupProfile(group=group)
        group_profile.save()
        discussion = Discussion(name="test_discussion", type=discussion_type, group=group)
        discussion.save()
    
    def test_send_notification_to_user(self):
        """
        Tests that notification is sent to user.
        """
        notification = Notification(text="There is a new story in discussion", \
                                    recipient = User.objects.get(username="test_user"), \
                                    group = Group.objects.get(name="test_group"))
        notification.save()
        # Test that one message has been sent.
        self.assertEquals(len(mail.outbox), 1)
        
        
    def test_send_notification_to_group(self):
        """
        Tests that notification is sent to group.
        """
        group=Group.objects.get(name="test_group")
        notification = Notification(text="There is a new story in discussion", \
                                    group=group)
        notification.save()
        # Test that one message has been sent.
        self.assertEquals(len(mail.outbox), len([user for user in User.objects.all() if group in user.groups.all()]))