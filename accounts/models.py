from django.db import models

from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings


class OtpList(models.Model):
    phone_number = models.CharField(max_length=12, unique=True)
    otp_token = models.CharField(max_length=10)
    datetime = models.DateTimeField()
    account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, unique=True)

    def __str__(self):
        return f"phone: {self.phone_number} | token:'{self.otp_token}'"


class BaseManger(BaseUserManager):

    def create_user(self, username, password=None, **extra_fields):

        if not username:
            raise ValueError("set a username")
        if extra_fields.get('phone_number', False) == False and not extra_fields.get('is_superuser'):
            raise ValueError("set a phone_number")

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=60, unique=True, null=True)
    email = models.EmailField(unique=True, null=True)
    first_name = models.CharField(max_length=60, null=True)
    last_name = models.CharField(max_length=60, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, unique=True)
    profile_image = models.ImageField(upload_to="profile", null=True)

    objects = BaseManger()
    USERNAME_FIELD = 'username'

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        return self.is_superuser

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        return self.is_superuser
    def __str__(self):
        return f"{self.phone_number}"