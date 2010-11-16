from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from feedback.forms import FeedbackForm
from feedback.models import Feedback

class FeedbackTests(TestCase):
    urls = 'feedback.tests.urls'
    def setUp(self):
        self.user = User.objects.create_user('spongebob', 'user@localhost.local', 'secret')

    def test_form(self):
        form = FeedbackForm(dict(message="Test Message"))
        form_valid = form.is_valid()
        self.assertTrue(form.is_valid())
        form.save()

    def test_form_view_initial(self):
        response = self.client.get(reverse('feedback'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feedback/feedback_form.html')
        self.failUnless(isinstance(response.context['form'], FeedbackForm))

    def test_thanks_view(self):
        response = self.client.get(reverse('feedback_thanks'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feedback/feedback_thanks.html')

    def test_logged_in(self):
        self.client.login(username='spongebob', password='secret')
        self.client.post(reverse('feedback'), {'message' : 'square pants'})
        feedback = Feedback.objects.get(pk=1)
        self.assertEqual(feedback.user, self.user)


