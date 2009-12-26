import django_filters

from models import GroupProfile
from django.contrib.auth.models import User

class GroupProfileFilter(django_filters.FilterSet):
    class Meta:
        model = GroupProfile
        fields = ['parent', 'location', 'created_by']
        
class MemberProfileFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ['is_active', 'is_staff', 'is_superuser']