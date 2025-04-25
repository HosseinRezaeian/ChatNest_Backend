

from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser,PermissionsMixin,BaseUserManager

from utils.abstract.models import AbstractHashId
from utils.abstract.serializers import AbstractHashidSerializer


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username,password=None, **extra_fields):
        if not email or not username:
            raise ValueError("email is required!")
        email = self.normalize_email(email)
        user = self.model(email=email,username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email,username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email,username, password, **extra_fields)

class CustomUser(AbstractUser,PermissionsMixin,AbstractHashId):
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="customuser_groups",  # Changed
        related_query_name="customuser",  # Changed
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_permissions",  # Changed
        related_query_name="customuser",  # Changed
    )

    def __str__(self):
        return self.email