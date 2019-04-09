from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import Profile


class UserForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = ['username', 'first_name', 'last_name', 'email_id', 'password1', 'password2', 'is_seller', 'profile_pic', ]


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)