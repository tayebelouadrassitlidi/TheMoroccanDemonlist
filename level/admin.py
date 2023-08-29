import datetime
from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import Level
import math

# Register your models here.

class CustomSortableAdminMixin(SortableAdminMixin):
    def _update_order(self, updated_items, extra_model_filters):
        old_rankings = {}
        for item in updated_items:
            level = Level.objects.get(pk=item[0])
            old_rankings[level.pk] = level.ranking

        super()._update_order(updated_items, extra_model_filters)
        for item in updated_items:
            level = Level.objects.get(pk=item[0])
            level.save()

        for level_record in level.levelrecord_set.all():
            level_record.save()             

class LevelAdmin(CustomSortableAdminMixin, admin.ModelAdmin):
    list_display = ['ranking', 'name', 'points', 'min_points', 'min_completion', 'first_victor']
    search_fields = ['name', 'levelid']
    ordering = ['ranking']
    actions = ['save_all']

    def save_all(self, request, queryset):
        for obj in queryset:
            obj.points = round(500 * (1 - math.log(obj.ranking, 151)), 2)
            obj.min_points = round((500 * (1 - math.log(obj.ranking, 151))) * 1/3, 2)
            obj.save()

            for level_record in obj.levelrecord_set.all():
                level_record.save()

        self.message_user(request, f"{queryset.count()} levels saved successfully.")

    save_all.short_description = "Save selected levels"
    
    def add_view(self, request, form_url='', extra_context=None):
            self.exclude = ['points', 'min_points']
            return super().add_view(request, form_url, extra_context)

admin.site.register(Level, LevelAdmin)