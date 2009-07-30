from models import *
from django.contrib import admin



class GoalAdmin(admin.ModelAdmin):
    list_display = ('name', 'group_profile', 'short_description', 'parent', 'forked_from', 'created_by', 'created_at', 'updated_at',)
    list_filter = ('created_by',)
    search_fields = ('name', 'group_profile', 'short_description',)
    ordering = ('name',) 
    
    
admin.site.register(Goal, GoalAdmin)


