from ecclesia.discussions.models import Story, Discussion
import django_filters
from django import forms


from django.contrib.contenttypes.models import ContentType

class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        exclude = ('x_pos', 'y_pos', 'width', 'height', 'last_related_update', 'slug', 'workflow_status')

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        exclude = ('x_pos', 'y_pos', 'width', 'height', 'created_by', 'discussion')

def get_story_form_for_object(object):
    content_type = ContentType.objects.get_for_model(object).id
    object_id = object.id
    return StoryForm(initial={'content_type':content_type, 'object_id':object_id})

class DiscussionFilter(django_filters.FilterSet):
    class Meta:
        model = Discussion
        fields = ['type', 'created_by']

class StoryFilter(django_filters.FilterSet):
    class Meta:
        model = Story
        fields = ['speech_act', 'created_by']