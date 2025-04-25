from django.db import models
from hashid_field import HashidAutoField
from config import settings


class AbstractCreateUpdateModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AbstractCreator(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_created")

    class Meta:
        abstract = True


class AbstractHashId(models.Model):
    id = HashidAutoField(primary_key=True,
                         salt=settings.SECRET_KEY,
                         min_length=8)

    class Meta:
        abstract = True
