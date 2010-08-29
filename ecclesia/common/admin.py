from models import *
from django.contrib import admin

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'followed_object', 'content_type')
    list_filter = ('user', 'content_type')
    search_fields = ('user', 'followed_object', 'content_type')
    ordering = ('user',)

admin.site.register(Subscription, SubscriptionAdmin)