import hashlib
from django.db import models
from django.contrib.auth.models import Group, User
from django.utils.translation import gettext_lazy as _
from common.utils import get_domain
from common.models import Presentable
from django.conf import settings

class UserProfile(models.Model):
    """
	Enhances the definitions of User.
	"""
    user = models.ForeignKey(User, unique=True, verbose_name=_('user'), related_name='profile', help_text=_("The internal User entity. Add this entity before you create a profile and set a User for it."))
    picture = models.ImageField(max_length=100, default='img/user_pics/default_photo.gif', upload_to='img/user_pics', help_text=_('The name of the image file.'))
    gravatar = models.EmailField(max_length=100, help_text=_('The email of your gravatar.'), null=True, blank=True)
    #im_address = models.CharField(_('im_address'), max_length=500, null=True, blank=True, help_text=_('IM address of the user'))
    #im_type = models.CharField(_('im type'), max_length=30, null=True, blank=True, choices = (("gtalk", "gtalk"),), help_text=_('IM type of the user'))

    def __unicode__(self):
        return "%s's profile" % (self.user.username,)

    def get_picture_abs_url(self):
        if self.gravatar:
            h = hashlib.md5()
            h.update(self.gravatar)
            return "http://www.gravatar.com/avatar/%s" % h.hexdigest()
        else:
            return "%s%s" % (settings.MEDIA_URL, self.picture)


class GroupProfile(Presentable):
    """
    Represents an organization of people trying to meet some
    common goals. This is an extension of the django.contrib.auth Group model,
	use the above to manage the actual group membership.
    """
    group = models.ForeignKey(Group, unique=True, verbose_name=_('group'), related_name='profile', help_text=_("The internal Group entity. If you are adding a Profile Group, please create a new Group & don't select an existing one"))
    slug = models.SlugField(_('slug'), unique=True, blank=False, help_text=_("The url representation of the group's name. No whitespaces allowed - use hyphen/underscore to separate words."))
    description = models.TextField(_('description'), max_length=1000, null=True, blank=True, help_text=_("The group's description"))
    parent = models.ForeignKey('self', verbose_name=_('parent'), related_name='children', null=True, blank=True, help_text=_('The parent group containing this group'))
    forked_from = models.ForeignKey('self', verbose_name=_('forked from'), related_name='forks', null=True, blank=True, help_text=_('The group from which this group forked'))
    location = models.CharField(_('location'), max_length=500, null=True, blank=True, help_text=_('Where is the group located'))
    #geolocation
    #tags
    created_by = models.ForeignKey(User, editable=False, verbose_name=_('created by'), null=True, blank=True, help_text=_('The user that created the group'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, help_text=_('When was the group created'))
    updated_at = models.DateTimeField(_('updated at'), auto_now=True, help_text=_('When was the group last updated'))

    class Meta:
        verbose_name = _("group profile")
        verbose_name_plural = _("group profiles")


    def get_absolute_url(self):
        return "http://%s/group/%s/" % (get_domain(), self.slug)

    def save(self):
        super(GroupProfile, self).save()
        if self.created_by:
            if not GroupPermission.objects.filter(group=self.group).filter(user=self.created_by):
                user = self.created_by
                user.groups.add(self.group)
                user.save()
                group_permission = GroupPermission(group=self.group, user=self.created_by, permission_type=1)
                group_permission.save()

    def __unicode__(self):
        return self.group.name

    def get_group_members(self):
        members = [user for user in User.objects.all() if self.group in user.groups.all()]
        return members

def get_user_groups(user):
    """
    Gets the group profiles associated with a user.
    """
    auth_groups = user.groups.all()
    # groups = [group.profile for group in auth_group] # not working
    # todo implement better
    groups = [GroupProfile.objects.filter(group=group)[0] for group in auth_groups if GroupProfile.objects.filter(group=group).count()]
    return groups

class MissionStatement(models.Model):
    """
    A suggested mission statement for a group. The members of the group can each
    create mission statements for the group, & also vote their support for mission
    statements. The actual group profile will feature the mission statement that
    has the largest support (i.e., number of votes).
    """
    group_profile = models.ForeignKey(GroupProfile, editable=False, verbose_name=_('group profile'), related_name='mission_statements', help_text=_('The groupd subject of this mission statement'))
    mission_statement = models.TextField(_('mission statement'), max_length=1000, help_text=_('The suggested mission statement of the group'))
    created_by = models.ForeignKey(User, verbose_name=_('created by'), null=True, blank=True, help_text=_('The user that created the mission statement'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, help_text=_('When was the mission statement created'))
    updated_at = models.DateTimeField(_('updated at'), auto_now=True, help_text=_('When was the mission statement last updated'))


    class Meta:
        verbose_name = _("mission statement")
        verbose_name_plural = _("mission statements")


    def get_absolute_url(self):
        return "http://%s/admin/groups/missionstatement/%d/" % (get_domain(), self.id)


    def __unicode__(self):
        return u"%s's %s" % (self.group_profile.group.name, _('mission statement'))

class GroupPermission(models.Model):
    """
    Group permissions. Only the manager of the group has the permission to delete a group,
    delete a discussion, kick member out from the group, promote member to manager and
    demote member from being a manager.
    """
    group = models.ForeignKey(Group, verbose_name=_('group'), related_name='permission', help_text=_("Group entity"))
    user = models.ForeignKey(User, verbose_name=_('user'), help_text=_('The user that has the permissions'))
    permission_type = models.IntegerField(choices = ((1, "Manager"), (2, "Editor"), (3, "Reader")))

    class Meta:
        verbose_name = _("group permission")
        verbose_name_plural = _("group permissions")

    def __unicode__(self):
        return u"%s's permission for %s" % (self.user, self.group)

#def add_user_profile(sender, instance, **kwargs):  
#    UserProfile(user=instance).save()
    
def create_profile(sender, **kw):
    user = kw["instance"]
    if kw["created"]:
        profile = UserProfile(user=user)
        profile.save()
        
#create user profile when user is created
models.signals.post_save.connect(create_profile, sender=User, dispatch_uid="users-profilecreation-signal")
