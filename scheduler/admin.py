from django.contrib import admin
from .models import Employee, Site, Duty


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'created_at']
    search_fields = ['name', 'position']
    list_filter = ['position']


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'created_at']
    search_fields = ['name', 'address']


@admin.register(Duty)
class DutyAdmin(admin.ModelAdmin):
    list_display = ['employee', 'site', 'date', 'notes']
    list_filter = ['site', 'employee', 'date']
    date_hierarchy = 'date'
    search_fields = ['employee__name', 'site__name']
