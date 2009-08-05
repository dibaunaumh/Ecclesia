from models import *
from django.contrib import admin
from django.contrib.contenttypes import generic
from discussion.models import Story


class StoryInline(generic.GenericTabularInline):
    model = Story
    extra = 1

class GoalAdmin(admin.ModelAdmin):
    list_display = ('name', 'group_profile', 'short_description', 'parent', 'forked_from', 'created_by', 'created_at', 'updated_at',)
    list_filter = ('created_by',)
    search_fields = ('name', 'group_profile', 'short_description',)
    ordering = ('name',)
    inlines = (StoryInline,)
    
    
admin.site.register(Goal, GoalAdmin)
