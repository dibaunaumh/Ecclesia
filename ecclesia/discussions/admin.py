from models import *
from django.contrib import admin
from django.utils.translation import gettext_lazy as __unicode__
from django.utils.translation import gettext_lazy as _

class DiscussionTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

class DiscussionAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'type', 'group', 'description', 'created_by', 'created_at', 'updated_at')
    list_filter = ('group', 'type', 'created_at', 'updated_at')
    search_fields = ('name', 'group', 'slug', 'description')
    ordering = ('name', 'slug', 'group', 'type', 'created_at', 'updated_at')
	
class SpeechActAdmin(admin.ModelAdmin):
    list_display = ('name', 'story_type', 'discussion_type', 'ordinal')
    list_filter = ('name', 'story_type', 'discussion_type')
    search_fields = ('name',)
    ordering = ('name', 'story_type', 'discussion_type')
	
class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'speech_act', 'discussion', 'created_by', 'created_at', 'updated_at', 'content')
    list_filter = ('discussion', 'speech_act', 'created_at', 'created_by')
    search_fields = ('title', 'content', 'slug')
    ordering = ('title', 'discussion', 'speech_act', 'slug', 'created_at', 'updated_at')
	
class StoryRelationAdmin(admin.ModelAdmin):
    list_display = ('from_story', 'to_story', 'title', 'slug', 'speech_act', 'discussion', 'created_by', 'created_at', 'updated_at', 'content')
    list_filter = ('from_story', 'to_story', 'discussion', 'speech_act', 'created_at', 'created_by')
    search_fields = ('from_story', 'to_story', 'title', 'content', 'slug')
    ordering = ('from_story', 'to_story', 'title', 'discussion', 'speech_act', 'slug', 'created_at', 'updated_at')

class OpinionAdmin(admin.ModelAdmin):
    list_display = ('parent_story', 'title', 'slug', 'speech_act', 'discussion', 'created_by', 'created_at', 'updated_at', 'content')
    list_filter = ('parent_story', 'discussion', 'speech_act', 'created_at', 'created_by')
    search_fields = ('parent_story', 'title', 'content', 'slug')
    ordering = ('parent_story', 'title', 'discussion', 'speech_act', 'slug', 'created_at', 'updated_at')

class DiscussionConclusionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Story, StoryAdmin)
admin.site.register(StoryRelation, StoryRelationAdmin)
admin.site.register(SpeechAct, SpeechActAdmin)
admin.site.register(Opinion, OpinionAdmin)
admin.site.register(DiscussionType, DiscussionTypeAdmin)
admin.site.register(Discussion, DiscussionAdmin)
admin.site.register(DiscussionConclusion, DiscussionConclusionAdmin)