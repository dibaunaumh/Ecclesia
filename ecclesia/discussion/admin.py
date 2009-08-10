from models import *
from django.contrib import admin

class StoryAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'object', 'created_at', 'updated_at',)
    list_filter = ('speech_act',)
    search_fields = ('content',)
    ordering = ('created_at',)

admin.site.register(Story, StoryAdmin)
