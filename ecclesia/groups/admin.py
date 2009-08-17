from models import *
from django.contrib import admin
from django.contrib.contenttypes import generic



class MissionStatementInline(admin.TabularInline):
    model = MissionStatement
    extra = 1


class MissionStatementAdmin(admin.ModelAdmin):
    pass


class GroupProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'parent', 'forked_from', 'location', 'created_by', 'created_at', 'updated_at',)
    list_filter = ('location', 'created_by',)
    search_fields = ('name', 'group', 'description', 'location',)
    ordering = ('name',)
    inlines = (MissionStatementInline,)
    

admin.site.register(GroupProfile, GroupProfileAdmin)
admin.site.register(MissionStatement, MissionStatementAdmin)
