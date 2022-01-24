from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, ProgressOfProject


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("name", "username", "email", "password1", "password2")

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
