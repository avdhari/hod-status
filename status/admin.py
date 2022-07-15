from django.contrib import admin
from .models import User, Project, ProgressOfProject


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Custom admin for User"""
    list_display = ['name', 'email', 'is_active', 'is_superuser', 'last_login']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Custom admin for Project"""
    list_display = ['name', 'client_name', 'client_id', 'assigned_to', 'is_live', 'is_removed']


@admin.register(ProgressOfProject)
class ProgressAdmin(admin.ModelAdmin):
    """Custom admin for Progress"""
    list_display = ['drawing',  'project', 'progress']
