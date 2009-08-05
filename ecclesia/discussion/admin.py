from models import *
from django.contrib import admin

class StoryAdmin(admin.ModelAdmin):
    list_display = ('speech_act', 'object', 'created_by', 'created_at', 'updated_at',)
    list_filter = ('created_by',)
    search_fields = ('content',)
    ordering = ('created_at',)

admin.site.register(Story, StoryAdmin)

class SpeechActAdmin(admin.ModelAdmin):
    pass

admin.site.register(SpeechAct, SpeechActAdmin)
