from models import *
from django.contrib import admin

class GoalAdmin(admin.ModelAdmin):
    ordering = ('name',)
admin.site.register(Goal, GoalAdmin)


