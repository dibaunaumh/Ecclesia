from models import *
from discussions.models import Discussion


def create_user(username, first_name, last_name):
    user = User(username=username)
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    return user


def create_group(name, created_by, members, slug):
    group = Group(name=name)
    group.save()
    group_profile = GroupProfile()
    group_profile.group = group
    group_profile.name = group.name
    group_profile.slug = slug
    group_profile.description = "A test group"
    group_profile.location = "Israel"
    group_profile.created_by = created_by
    group_profile.save()
    for member in members:
        join_group(group, member)
    return group_profile


def join_group(group, member):
    member.groups.add(group)
    member.save()


def create_discussion(name, group, created_by, slug):
    discussion = Discussion()
    discussion.name = name
    discussion.slug = slug
    discussion.description = "Test discussions %s" % name
    discussion.group = group
    discussion.created_by = created_by
    discussion.save()
    return discussion