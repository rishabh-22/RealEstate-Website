from django.db import models
from django.contrib.auth.models import User


class Profile(User):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, parent_link=True)
    is_seller = models.BooleanField(default=False, verbose_name='Seller')
    profile_pic = models.ImageField(upload_to='media/user_profilePics/', default='static/profile_pic.jpeg')
    description = models.TextField(null=True, blank=True)
    email_id = models.EmailField(unique=True)
    phone_num = models.IntegerField(null=True)
