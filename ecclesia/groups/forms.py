import django_filters
from django import forms
from models import GroupProfile
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

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
