from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Profile


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', ]


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['is_seller', 'description', 'profile_pic', 'email', ]
