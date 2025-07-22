from django.contrib.auth import get_user_model
from hashid_field.rest import HashidSerializerCharField
from  rest_framework import serializers

from apps.accounts.api.serializer import UserReadSerializer
# from apps.accounts.api.serializer import UserReadSerializer
from apps.chats.models import  Message,PrivateRoom
from config import settings
from utils.abstract.models import AbstractCreateUpdateModel
from utils.abstract.serializers import AbstractHashidSerializer
User = get_user_model()


class UserRoomSerializer(AbstractHashidSerializer):
    class Meta:
        model = User
        fields = [
            "id","username",
        ]


class MessageSerializer(AbstractHashidSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class PrivateRoomSerializer(AbstractHashidSerializer):
    user1=UserRoomSerializer(read_only=True)
    user2=UserRoomSerializer(read_only=True)
    class Meta:
        model = PrivateRoom
        fields = ["name","id","user1","user2"]


class PrivateRoomSerializerCreate(AbstractHashidSerializer):
    email = serializers.EmailField()
    class Meta:
        model = PrivateRoom
        fields = ['email']

    def create(self, validated_data):
        user1 = User.objects.get(email=validated_data['email'])
        user2 = self.context['request'].user
        room, _ = PrivateRoom.objects.get_or_create(
            user1=min(user1, user2, key=lambda u: u.id),
            user2=max(user1, user2, key=lambda u: u.id),creator=user2,name=f'{user1} {user2}'
        )
        return room


class MessageSerializer(AbstractHashidSerializer):
    class Meta:
        model = Message
        fields = '__all__'