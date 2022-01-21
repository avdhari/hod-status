from django.contrib import admin
from .models import User, Project, ProgressOfProject


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Custom admin for User"""
    list_display = ['name', 'email', 'is_superuser']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Custom admin for Project"""
    list_display = ['name', 'client_name', 'client_id', 'assigned_to', 'is_live']


@admin.register(ProgressOfProject)
class ProgressAdmin(admin.ModelAdmin):
    """Custom admin for Progress"""
    list_display = ['drawing',  'project', 'progress']
