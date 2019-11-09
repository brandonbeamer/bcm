import re

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class CredForm(UserCreationForm):
    def clean_username(self):
        username = self.cleaned_data['username']

        if not re.search(r'^[a-zA-Z].{3,}$', username):
            raise forms.ValidationError('Usernames must be at least 4 characters, and start with a letter.')
        return username
