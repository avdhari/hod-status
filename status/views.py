from cmath import log
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth import login
from django.contrib import messages
from django.template import context
from .forms import NewUserForm, NewProgressForm
from .models import Project, ProgressOfProject


@login_required
def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    context = {
        "register_form": form,
        }
    return render(request, "status/user_registration.html", context)


def base_view(request):
    return render(request, 'status/base.html')


@login_required
def home_view(request):
    current_user = request.user
    projects = Project.objects.all().order_by('-id')
    project = Project.objects.get(assigned_to=current_user)
    progress = ProgressOfProject.objects.all().order_by('-id')

    context = {
        'projects': projects,
        'progress': progress,
    }

    if current_user.is_superuser:
        return render(request, 'status/admin.html', context)
    else:
        return render(request, 'status/staff.html', context)


@login_required
def new_progress(request):
    if request.method == "POST":
        progress_form = NewProgressForm(request.POST, request.FILES)
        if progress_form.is_valid():
            progress_form.save()
            return redirect('/')
    progress_form = NewProgressForm()
    context = {
        'progress_form': progress_form,
    }
    return render(request, 'status/new_progress.html', context)
