from django.contrib import admin
from .models import ListChange
from django.forms import CharField
from level.models import Level

# Register your models here.

class ListChangeAdmin(admin.ModelAdmin):
    list_display = ['date', 'level', 'description', 'effect']
    search_fields = ['date', 'level']

    def add_view(self, request, form_url='', extra_context=None):
            self.exclude = ['description']
            return super().add_view(request, form_url, extra_context)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "level":
            return CharField(max_length=255)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(ListChange, ListChangeAdmin)