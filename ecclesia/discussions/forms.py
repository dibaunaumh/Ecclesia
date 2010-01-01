from ecclesia.discussions.models import Story

from django import forms

from django.contrib.contenttypes.models import ContentType

class StoryForm(forms.ModelForm):
    content_type = forms.ModelChoiceField(queryset=ContentType.objects.all(), widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    
    class Meta:
        model = Story

def get_story_form_for_object(object):
    content_type = ContentType.objects.get_for_model(object).id
    object_id = object.id
    return StoryForm(initial={'content_type':content_type, 'object_id':object_id})
