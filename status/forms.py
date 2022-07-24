from django import forms
from .models import Project, User, ProgressOfProject


BOOL_LIST = (
    (True, 'Yes'),
    (False, 'No')
)

STATUS_TYPE = [
    ('in_progress', 'In Progress'),
    ('on_hold', 'On Hold'),
    ('done', 'Done!')
]


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


class EditProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'client_name', 'client_id', 'assigned_to', 'deadline', 'status', 'is_removed',)
        # is_live = forms.ChoiceField(choices=BOOL_LIST)
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'status': forms.Select(choices=STATUS_TYPE),
            'is_removed': forms.Select(choices=BOOL_LIST),
        }
