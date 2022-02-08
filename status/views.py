from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, HttpResponseNotAllowed
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail

from .forms import NewProjectForm, NewUserForm, NewProgressForm
from .models import Project, ProgressOfProject, User


class SuperUserMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


def base_view(request):
    return render(request, 'status/base.html')


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
    return render(request, "registration/user_registration.html", context)


def password_reset(request):
    return render(request, 'registration/password_reset.html')


@login_required
def home_view(request):
    current_user = request.user
    projects = Project.objects.filter(is_removed=False).order_by('-id')
    progress = ProgressOfProject.objects.filter(is_removed=False).order_by('-id')
    staffs = User.objects.filter(is_active=True).order_by('date_joined')
    context = {
        'projects': projects,
        'progress': progress,
        'staffs': staffs,
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


@login_required
def new_project(request):
    if request.method == "POST":
        project_form = NewProjectForm(request.POST)
        if project_form.is_valid():
            project_form.save()
            return redirect('/')
    project_form = NewProjectForm()
    context = {
        'project_form': project_form,
    }

    return render(request, 'status/new_project.html', context)


def project_detail_view(request, slug):
    project = Project.objects.get(slug=slug)
    context = {
        'project':project,
    }
    return render(request, 'status/project_detail.html', context)

@login_required
def user_list_view(request):
    current_user = request.user
    staffs = User.objects.filter(is_active=True).order_by('date_joined')

    context = {
        'staffs': staffs,
    }
    if current_user.is_superuser:
        return render(request, 'status/userlist.html', context)
    else:
        return HttpResponse("Not allowed")


@login_required
def user_detail_view(request, pk):
    current_user = request.user
    staff = User.objects.get(id=pk)
    projects = Project.objects.filter(assigned_to=staff)
    context = {
        'staff': staff,
        'projects': projects,
    }
    if current_user.is_superuser:
        return render(request, 'status/user_detail.html', context)
    else:
        return HttpResponse("Not allowed")
