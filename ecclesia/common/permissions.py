from ecclesia.permissions.models import *
from ecclesia.permissions.utils import register_role, get_role

def create_permission(role_object, content_object, permission_name):
    if role_object == 'Everyone':
        if not Role.objects.filter(name='Everyone'):
            role = Role(name='Everyone').save()
        else:
            role = Role.objects.get(name='Everyone')
    if role_object.__class__.__name__ == "GroupProfile":
        if not Role.objects.filter(name='group_%s' % role_object.pk):
            role = register_role('group_%s' % role_object.pk)
        else:
            role = get_role('group_%s' % role_object.pk)
    
    permission, created = Permission.objects.get_or_create(name=permission_name, codename=permission_name)
    ObjectPermission(role=role, content=content_object, permission=permission).save()
