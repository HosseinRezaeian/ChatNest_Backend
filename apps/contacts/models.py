from django.contrib.auth.models import AbstractUser
from django.db import models

from config import settings
from utils.abstract.models import AbstractHashId


# Create your models here.
class Contact(AbstractHashId):
    source = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='user_source')
    target = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='user_target')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['source', 'target'], name='unique_contact')
        ]