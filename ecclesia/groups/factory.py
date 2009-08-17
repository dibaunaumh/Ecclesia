from models import *
from goals.models import Goal


def create_user(username, first_name, last_name):
    user = User(username=username)
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    return user


def create_group(name, created_by, members):
    group = Group(name=name)
    group.save()
    group_profile = GroupProfile()
    group_profile.group = group
    group_profile.name = group.name
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


def create_goal(name, group, created_by):
    goal = Goal()
    goal.name = name
    goal.short_description = "Test goal %s" % name
    goal.group_profile = group
    goal.created_by = created_by
    goal.save()
    return goal