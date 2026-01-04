# core Django
from django.contrib.auth.models import(
    AbstractBaseUser, 
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone

# accounts app
from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    profile_picture = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    username = models.CharField(max_length=25, null=True, blank=True)
    email = models.EmailField(unique=True)
    bio = models.CharField(max_length=100, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def user_joined_recently(self):
        return (timezone.now() - self.date_joined).days < 30
    
