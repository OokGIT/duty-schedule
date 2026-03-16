from django.contrib import admin
from .models import Employee, Site, Duty


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'patronymic', 'position', 'created_at']
    search_fields = ['last_name', 'first_name', 'patronymic', 'position']
    list_filter = ['position']


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_name', 'address', 'display_mode', 'color', 'created_at']
    search_fields = ['name', 'short_name', 'address']
    list_filter = ['display_mode']


@admin.register(Duty)
class DutyAdmin(admin.ModelAdmin):
    list_display = ['employee', 'site', 'date', 'notes']
    list_filter = ['site', 'employee', 'date']
    date_hierarchy = 'date'
    search_fields = ['employee__name', 'site__name']
