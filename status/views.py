from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .forms import NewUserForm
from .models import Project, ProgressOfProject


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
    projects = Project.objects.all()
    progress = ProgressOfProject.objects.all()
    context = {
        'projects': projects,
        'progress': progress,
    }

    current_user = request.user
    if current_user.is_superuser:
        return render(request, 'status/admin.html', context)
    else:
        return render(request, 'status/staff.html', context)
