from django.shortcuts import render
from .models import Staff, Project


def base_view(request):
    return render(request, 'status/base.html')


def home_view(request):
    projects = Project.objects.all()
    context = {
        'projects': projects,
    }
    return render(request, 'status/index.html', context)
