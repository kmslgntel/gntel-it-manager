from django.contrib import admin
from .models import Rack, Switch, SwitchPort, SwitchMacEntry, SwitchConfigBackup


@admin.register(Rack)
class RackAdmin(admin.ModelAdmin):
    list_display = ('legacy_rack_id', 'name')
    search_fields = ('name',)


@admin.register(Switch)
class SwitchAdmin(admin.ModelAdmin):
    list_display = ('legacy_switch_id', 'ip', 'rack', 'sort_order', 'vendor')
    list_filter = ('rack', 'vendor')
    search_fields = ('ip',)


@admin.register(SwitchPort)
class SwitchPortAdmin(admin.ModelAdmin):
    list_display = ('switch', 'interface', 'port_mode', 'area_number', 'port_number')
    list_filter = ('port_mode', 'switch__rack')
    search_fields = ('interface', 'area_number')
    raw_id_fields = ('switch',)


@admin.register(SwitchMacEntry)
class SwitchMacEntryAdmin(admin.ModelAdmin):
    list_display = ('switch', 'interface', 'vlan', 'mac', 'entry_type')
    search_fields = ('mac', 'interface')
    raw_id_fields = ('switch',)


@admin.register(SwitchConfigBackup)
class SwitchConfigBackupAdmin(admin.ModelAdmin):
    list_display = ('switch', 'backup_date', 'backup_time', 'status', 'created_at')
    list_filter = ('status', 'backup_date')
    search_fields = ('switch__ip',)
    raw_id_fields = ('switch',)
