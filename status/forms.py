from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Project, User, ProgressOfProject

from bootstrap_datepicker_plus.widgets import DatePickerInput


IS_LIVE = (
    (True, 'Yes'),
    (False, 'No')
)


class NewUserForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("name", "username", "email")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class NewProgressForm(forms.ModelForm):

    class Meta:
        model = ProgressOfProject
        fields = ('project', 'drawing', 'progress', 'image')

    def __init__(self, user, *args, **kwargs):
        super(NewProgressForm, self).__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.filter(assigned_to=user, is_removed=False)


class NewProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'client_name', 'client_id', 'assigned_to', 'deadline', )
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }
