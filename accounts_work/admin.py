from django.contrib import admin
from .models import AccountWork


@admin.register(AccountWork)
class AccountWorkAdmin(admin.ModelAdmin):
    list_display = ('work_date', 'system_type', 'work_type', 'operator', 'target', 'detail_short')
    list_filter = ('system_type', 'work_type', 'operator')
    search_fields = ('operator', 'target', 'detail')
    date_hierarchy = 'work_date'
    ordering = ('-work_date',)

    def detail_short(self, obj):
        return obj.detail[:60] if obj.detail else ''
    detail_short.short_description = '세부내용'
