import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


INDIFFERENT = 3
SENTIMENTS = ((1, _("Furious")), (2, _("Disappointed")), (INDIFFERENT, _("Indifferent")), (4, _("Happy")), (5, "Exctatic"))

BUG = 1
FEEDBACK_SPEECH_ACTS = ((BUG, _("Bug")), (2, _("Complaint")), (3, _("Request")), (4, _("Suggestion")), (5, _("Compliment")))


class Feedback(models.Model):
    """Feedback from a user"""
    sentiment = models.IntegerField(_("Sentiment"), choices=SENTIMENTS, default=INDIFFERENT)
    speech_act = models.IntegerField(_("Feedback type"), choices=FEEDBACK_SPEECH_ACTS, default=BUG)
    message = models.TextField(_("Message"))
    created = models.DateTimeField(editable=False,default=datetime.datetime.now)
    user = models.ForeignKey(User, blank=True, null=True)
    browser = models.CharField(max_length=255, blank=True, null=True)


    def __unicode__(self):
        return self.message