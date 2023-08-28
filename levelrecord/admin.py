from django.contrib import admin
from .models import LevelRecord

# Register your models here.

class LevelRecordAdmin(admin.ModelAdmin):
    list_display = ['player', 'level', 'record_percentage']
    search_fields = ['player__name', 'level__name']

admin.site.register(LevelRecord, LevelRecordAdmin)