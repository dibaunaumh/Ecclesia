from django.contrib.auth.models import User
from groups.models import UserProfile, GroupProfile
from django.http import HttpResponse

def user_can_view_group(request, user_profile_pk, group_profile_pk):
    user = UserProfile.objects.get(pk=user_profile_pk)
    group = GroupProfile.objects.get(pk=group_profile_pk)
    if group.is_private and user.user not in group.get_group_members():
        return HttpResponse("False")
    return HttpResponse("True")
