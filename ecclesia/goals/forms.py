from models import Goal,CourseOfAction,PossibleResult

from django import forms

#from django.contrib.contenttypes.models import ContentType

class CourseOfActionForm(forms.ModelForm):
    #content_type = forms.ModelChoiceField(queryset=ContentType.objects.all(), widget=forms.HiddenInput)
    #object_id = forms.IntegerField(widget=forms.HiddenInput)
    goal = forms.ModelChoiceField(queryset=Goal.objects.all(), widget=forms.HiddenInput)
    class Meta:
        model = CourseOfAction
        fields = ('name', 'short_description')


def get_course_of_action_form(goal):
    #content_type = ContentType.objects.get_for_model(object).id
    #object_id = object.id
    return CourseOfActionForm(initial={'goal':goal.id})

class PossibleResultForm(forms.ModelForm):
    #content_type = forms.ModelChoiceField(queryset=ContentType.objects.all(), widget=forms.HiddenInput)
    #object_id = forms.IntegerField(widget=forms.HiddenInput)
    goal = forms.ModelChoiceField(queryset=Goal.objects.all(), widget=forms.HiddenInput)
    class Meta:
        model = PossibleResult
        fields = ('name', 'short_description')


def get_possible_result_form(goal):
    #content_type = ContentType.objects.get_for_model(object).id
    #object_id = object.id
    return PossibleResultForm(initial={'goal':goal.id})
