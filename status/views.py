from django.shortcuts import render, redirect
# from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
# from django.contrib.auth import login
from django.contrib import messages

from .forms import NewProjectForm, NewUserForm, NewProgressForm, EditProjectForm
from .models import Project, ProgressOfProject, User
from .tasks import send_onboarding_mail, resend_password_reset_mail


class SuperUserMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


def base_view(request):
    return render(request, 'status/base.html')


@login_required
@user_passes_test(lambda user: user.is_superuser)
def register_request(request):
    projects = Project.objects.all()
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            send_onboarding_mail.apply_async(args=[form.instance.id])
            return redirect("/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    context = {
        'register_form': form,
        'projects': projects,
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
    if request.POST and request.FILES:
        progress_form = NewProgressForm(request.user, request.POST, request.FILES)
        if progress_form.is_valid():
            progress_form.save()
            return redirect('/')
    progress_form = NewProgressForm(request.user)
    context = {
        'progress_form': progress_form,
    }
    return render(request, 'status/new_progress.html', context)


@login_required
@user_passes_test(lambda user: user.is_superuser)
def new_project(request):
    if request.method == "POST":
        project_form = NewProjectForm(request.POST)
        if project_form.is_valid():
            project_form.save()
            return redirect('/')
    project_form = NewProjectForm()
    current_user = request.user
    projects = Project.objects.filter(assigned_to=current_user)
    context = {
        'project_form': project_form,
        'projects': projects,
    }

    return render(request, 'status/new_project.html', context)


@login_required
@user_passes_test(lambda user: user.is_superuser)
def project_detail_view(request, slug):
    project = Project.objects.get(slug=slug)
    progress = ProgressOfProject.objects.filter(project=project)
    context = {
        'project': project,
        'progress': progress,
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
def user_detail_view(request, username):
    current_user = request.user
    staff = User.objects.get(username=username)
    projects = Project.objects.filter(assigned_to=staff)
    context = {
        'staff': staff,
        'projects': projects,
    }
    if current_user.is_superuser:
        return render(request, 'status/user_detail.html', context)
    else:
        return HttpResponse("Not allowed")


@login_required
def edit_project_view(request, slug):
    project = Project.objects.get(slug=slug)
    if request.method == 'POST':
        edit_form = EditProjectForm(request.POST, instance=project)
        if edit_form.is_valid():
            edit_form.save()
            return redirect(f'/projects/{slug}')
    edit_form = EditProjectForm(instance=project)
    context = {
        'edit_form': edit_form,
        'project': project,
    }
    return render(request, 'status/edit_project.html', context)


@login_required
@user_passes_test(lambda user: user.is_superuser)
def resend_password_reset(request, pk):
    staff = User.objects.get(id=pk)
    resend_password_reset_mail.apply_async(args=[staff.pk])
    return render(request, 'registration/password_reset_sent.html')
