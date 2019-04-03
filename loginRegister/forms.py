from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = ['username', 'first_name', 'last_name', 'email_id', 'password1', 'password2', 'is_seller', 'profile_pic', ]
        # exclude = '__all__'

