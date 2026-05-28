from django.contrib import admin
from .models import Company, Department, Person, IpGroup, IpAddress, NetworkDevice, Phone


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'company', 'use_yn')
    list_filter = ('company', 'use_yn')
    search_fields = ('code', 'name')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('legacy_id', 'name', 'person_type', 'department', 'company', 'use_yn')
    list_filter = ('person_type', 'use_yn', 'company')
    search_fields = ('legacy_id', 'name', 'emp_no', 'email')


@admin.register(IpGroup)
class IpGroupAdmin(admin.ModelAdmin):
    list_display = ('legacy_group_id', 'name', 'parent_name', 'is_phone_group')
    list_filter = ('is_phone_group',)
    search_fields = ('legacy_group_id', 'name', 'parent_name')


@admin.register(IpAddress)
class IpAddressAdmin(admin.ModelAdmin):
    list_display = ('ip', 'ip_int', 'group', 'person', 'note')
    list_filter = ('group',)
    search_fields = ('ip', 'note')
    raw_id_fields = ('person', 'group')


@admin.register(NetworkDevice)
class NetworkDeviceAdmin(admin.ModelAdmin):
    list_display = ('ip', 'mac', 'hostname', 'division', 'scan_user')
    search_fields = ('ip', 'mac', 'hostname')


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ('phone_id', 'person', 'ip_address', 'purpose', 'note')
    search_fields = ('phone_id', 'purpose', 'note')
    raw_id_fields = ('person', 'ip_address')
