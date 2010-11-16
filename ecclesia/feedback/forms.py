import datetime
from django.forms import ModelForm
from models import Feedback

class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ('sentiment', 'speech_act', 'message',)
"""
    def clean_created(self):
        if self.created is None:
            self.created = datetime.datetime.now()

"""
