from django.contrib import admin
from django.db.models import JSONField
from jsoneditor.forms import JSONEditor

from app.models import BedAvailability, BedAvailabilityCache, SyncPull


class CustomJSONEditor(JSONEditor):
    jsoneditor_options = {
        'mode': 'code',
    }


class BedAvailabilityCommonAdmin(admin.ModelAdmin):
    list_display = (
        'meta_synced_at', 'institution', 'district', 'last_updated', 'meta_last_updated_at', 'meta_created_at',
    )
    list_display_links = ('meta_synced_at', 'institution',)
    list_filter = ('meta_synced_at', 'district', 'institution',)
    ordering = ('-meta_synced_at', '-id',)
    formfield_overrides = {
        JSONField: {
            'widget': CustomJSONEditor
        }
    }


class SyncPullAdmin(admin.ModelAdmin):
    list_display = (
        'timestamp', 'created_bed_count', 'created_bed_cache_count', 'sync_start_time', 'sync_end_time',
        'sync_time_taken_seconds',
    )
    list_display_links = ('timestamp',)
    list_filter = ('timestamp',)
    ordering = ('-timestamp', '-id',)
    formfield_overrides = {
        JSONField: {
            'widget': CustomJSONEditor
        }
    }


admin.site.register(BedAvailability, BedAvailabilityCommonAdmin)
admin.site.register(BedAvailabilityCache, BedAvailabilityCommonAdmin)
admin.site.register(SyncPull, SyncPullAdmin)
