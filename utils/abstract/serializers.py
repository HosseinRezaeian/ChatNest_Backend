
from rest_framework import serializers
from hashid_field.rest import HashidSerializerCharField

from config import settings


class AbstractHashidSerializer(serializers.ModelSerializer):
    id = HashidSerializerCharField(
        salt=settings.SECRET_KEY,
        min_length=8
    )
    class Meta:
        abstract = True