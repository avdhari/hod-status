import imp
from operator import mod
from pyexpat import model
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail

from .forms import NewUserForm, NewProgressForm
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
    projects = Project.objects.all().order_by('-id')
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


class UserListView(SuperUserMixin, generic.ListView, ):
    model = User
    template_name = 'status/userlist.html'
    ordering = 'date_joined'


user_list_view = UserListView.as_view()


class UserDeatailView(SuperUserMixin, generic.DetailView):
    model = User
    template_name = 'status/user_detail.html'


user_detail_view = UserDeatailView.as_view()
