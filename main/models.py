from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractUser, UserManager


class User(AbstractUser):
    objects = UserManager()
    ROLE_CHOICES = [
        ('normal_user', 'Normal User'),
        ('shop_owner', 'Shop Owner'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='normal_user')
    money = models.DecimalField(default=0, max_digits=10, decimal_places=2)  # Add the money field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
    
    def is_admin(self):
        return self.role == 'shop_owner'
    
    objects = CustomUserManager()