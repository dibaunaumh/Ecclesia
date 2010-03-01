import django_filters
from django import forms
from models import GroupProfile, MissionStatement
from django.contrib.auth.models import User, Group

class GroupProfileFilter(django_filters.FilterSet):
    class Meta:
        model = GroupProfile
        fields = ['parent', 'location', 'created_by']

class MemberProfileFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ['is_active', 'is_staff', 'is_superuser']

class MemberProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',]

class GroupProfileForm(forms.ModelForm):
    class Meta:
        model = GroupProfile
        exclude = ('x_pos', 'y_pos', 'width', 'height', 'group', 'parent', 'forked_from', 'location')

class MissionStatementForm(forms.ModelForm):
    class Meta:
        model = MissionStatement
        exclude = ('created_by')
