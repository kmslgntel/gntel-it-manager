from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('acted_at', 'actor', 'action', 'target_type', 'target_id', 'detail_short')
    list_filter = ('action', 'target_type', 'actor')
    search_fields = ('actor', 'target_id', 'detail')
    readonly_fields = ('acted_at',)
    ordering = ('-acted_at',)

    def detail_short(self, obj):
        return obj.detail[:80] if obj.detail else ''
    detail_short.short_description = '상세'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
