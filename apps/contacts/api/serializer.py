from rest_framework import serializers

from apps.accounts.api.serializer import UserReadSerializer
from apps.contacts.models import Contact
from utils.abstract.serializers import AbstractHashidSerializer


class ContactSerializer(AbstractHashidSerializer):
    target = UserReadSerializer( read_only=True)
    class Meta:
        model = Contact
        fields = [
            "id",
            "target",
        ]