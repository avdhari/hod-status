from django.contrib import admin
from .models import Staff, Project, ProgressOfProject


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    """Custom admin for Staff"""
    list_display = ['name', 'email']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Custom admin for Project"""
    list_display = ['name', 'client_name', 'client_id', 'assigned_to', 'is_live']


@admin.register(ProgressOfProject)
class ProgressAdmin(admin.ModelAdmin):
    """Custom admin for Progress"""
    list_display = ['project',  'drawing', 'progress']
