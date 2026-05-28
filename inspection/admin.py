from django.contrib import admin
from .models import Server, Inspection, InspectionDetail


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ('name', 'excel_label', 'sort_order', 'collect_method', 'is_active')
    list_editable = ('sort_order', 'is_active')
    ordering = ('sort_order',)


class InspectionDetailInline(admin.TabularInline):
    model = InspectionDetail
    extra = 0
    fields = ('server', 'ip_status', 'cpu_usage_pct', 'ram_used_gb', 'disk_health',
              'account_create_cnt', 'account_change_cnt', 'account_delete_cnt')


@admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):
    list_display = ('inspect_ym', 'created_by', 'created_at', 'updated_at')
    search_fields = ('inspect_ym',)
    inlines = [InspectionDetailInline]


@admin.register(InspectionDetail)
class InspectionDetailAdmin(admin.ModelAdmin):
    list_display = ('inspection', 'server', 'ip_status', 'disk_health',
                    'account_create_cnt', 'account_change_cnt', 'account_delete_cnt')
    list_filter = ('inspection', 'server')
    raw_id_fields = ('inspection', 'server')
