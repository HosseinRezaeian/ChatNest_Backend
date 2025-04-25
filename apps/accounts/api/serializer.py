from django.contrib.auth import get_user_model


from config import settings
from utils.abstract.serializers import AbstractHashidSerializer

User = get_user_model()
class UserReadSerializer(AbstractHashidSerializer):
    class Meta:
        model = User
        fields=[

            "id",
            "username",
            "email",
            "first_name",
            "last_name",
        ]