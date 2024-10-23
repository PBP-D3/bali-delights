from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


class User(AbstractUser):
    ROLE_CHOICES = [
        ('normal_user', 'Normal User'),
        ('shop_owner', 'Shop Owner'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='normal_user')
    money = models.IntegerField(default=0)  # Add the money field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
    
    def is_admin(self):
        return self.role == 'shop_owner'
    
    objects = CustomUserManager()