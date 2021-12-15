from django.contrib import admin
from .models import Staff, Project, ProgressOfProject


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'client_name', 'client_id', 'assigned_to', 'is_live']


@admin.register(ProgressOfProject)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ['project', 'progress']