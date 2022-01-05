from django.shortcuts import render
from .models import Project, ProgressOfProject


def base_view(request):
    return render(request, 'status/base.html')


def home_view(request):
    projects = Project.objects.all()
    progress = ProgressOfProject.objects.all()
    context = {
        'projects': projects,
        'progress': progress,
    }
    return render(request, 'status/index.html', context)
