from models import *
from django.contrib import admin
from django.contrib.contenttypes import generic


class MissionStatementInline(admin.TabularInline):
    model = MissionStatement
    extra = 1


class MissionStatementAdmin(admin.ModelAdmin):
    pass


class GroupProfileAdmin(admin.ModelAdmin):
    list_display = ('slug', 'group', 'parent', 'forked_from', 'location', 'created_by', 'created_at', 'updated_at')
    list_filter = ('location', 'created_by',)
    search_fields = ('slug', 'group', 'description', 'location',)
    ordering = ('slug',)
    inlines = (MissionStatementInline,)
 
class UserProfileAdmin(admin.ModelAdmin):
    pass

	
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(GroupProfile, GroupProfileAdmin)
admin.site.register(GroupPermission)
admin.site.register(MissionStatement, MissionStatementAdmin)
