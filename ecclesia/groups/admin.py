from django.contrib import admin
from groups.models import *



class GroupProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'parent', 'forked_from', 'location', 'created_by', 'created_at', 'updated_at',)
    list_filter = ('location', 'created_by',)
    search_fields = ('name', 'group', 'description', 'location',)
    ordering = ('name',)
    
    

    

admin.site.register(GroupProfile, GroupProfileAdmin)
