from models import *
from django.contrib import admin
from django.contrib.contenttypes import generic
from discussions.models import Story


class StoryInline(generic.GenericTabularInline):
    model = Story
    extra = 1

class GoalAdmin(admin.ModelAdmin):
    list_display = ('name', 'group_profile', 'short_description', 'parent', 'forked_from', 'created_by', 'created_at', 'updated_at',)
    list_filter = ('created_by',)
    search_fields = ('name', 'group_profile', 'short_description',)
    ordering = ('name',)
    inlines = (StoryInline,)
    
    
class CourseOfActionAdmin(admin.ModelAdmin):
    pass


class PossibleResultAdmin(admin.ModelAdmin):
    pass


class CausingRelationAdmin(admin.ModelAdmin):
    pass


class LeadingRelationAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Goal, GoalAdmin)
admin.site.register(CourseOfAction, CourseOfActionAdmin)
admin.site.register(PossibleResult, PossibleResultAdmin)
admin.site.register(CausingRelation, CausingRelationAdmin)
admin.site.register(LeadingRelation, LeadingRelationAdmin)
