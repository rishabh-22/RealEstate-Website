from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    is_seller = models.BooleanField(default=False, verbose_name='Seller')
    profile_pic = models.ImageField(default='static/profile_pic.jpeg')
    description = models.TextField(null=True, blank=True)
    email = models.EmailField(unique=True)
