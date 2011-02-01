from django import forms
from models import Voting

class VotingForm(forms.Form):
    votes_per_participant = forms.IntegerField(min_value=0)
    days = forms.IntegerField(min_value=0, required=False)
    hours = forms.IntegerField(min_value=0, max_value=24, required=False)
    minutes = forms.IntegerField(min_value=0, max_value=59, required=False)

    def clean(self):
        if self.cleaned_data['days'] == 0 and self.cleaned_data['hours'] == 0 \
                and self.cleaned_data['minutes'] == 0:
            message = "Voting time can't be 0"
            raise forms.ValidationError, message
        else:
            return super(VotingForm, self).clean()