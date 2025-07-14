from django.contrib.auth import get_user_model
from hashid_field.rest import HashidSerializerCharField
from  rest_framework import serializers

from apps.accounts.api.serializer import UserReadSerializer
from apps.chats.api.validations.privateRoom import validatePrivateRoom
# from apps.accounts.api.serializer import UserReadSerializer
from apps.chats.models import Room, Message, UserRoom
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


class RoomSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    members = UserRoomSerializer(many=True)
    class Meta:
        model = Room
        fields = [
            "name",
            "type",
            "creator",
            "members"
        ]
    def validate(self, data):
        validatePrivateRoom(data)
        return data

    def create(self, validated_data):
        members = validated_data.pop("members")
        room = Room.objects.create(**validated_data)
        user_rooms = [
            UserRoom(room=room, user_id=user_id["id"])
            for user_id in members
        ]
        if validated_data.get("creator").id not in members:
            user_rooms.append(UserRoom(room=room, user=validated_data["creator"]))
        UserRoom.objects.bulk_create(user_rooms)
        return room

    def update(self, instance, validated_data):
        members = validated_data.pop("members", [])
        instance.name = validated_data.get('name', instance.name)
        instance.type = validated_data.get('type', instance.type)

        instance.save()

        existing_user_ids = [user_room.user.id for user_room in instance.user_room_set.all()]
        new_user_ids = [user_data['id'] for user_data in members]

        users_to_remove = set(existing_user_ids) - set(new_user_ids)
        UserRoom.objects.filter(room=instance, user_id__in=users_to_remove).delete()

        user_rooms = []
        for user_data in members:
            user_id = user_data['id']
            if not UserRoom.objects.filter(room=instance, user_id=user_id).exists():
                user_rooms.append(UserRoom(room=instance, user_id=user_id))

        if validated_data.get("creator") and validated_data["creator"].id not in new_user_ids:
            user_rooms.append(UserRoom(room=instance, user=validated_data["creator"]))

        UserRoom.objects.bulk_create(user_rooms)
        return instance





class RoomReadSerializer(AbstractHashidSerializer):
    members = UserRoomSerializer(many=True)
    creator = UserReadSerializer()
    class Meta:
        model = Room
        fields = [
            "name",
            "id",
            "creator",
            "members",
        ]




class MessageSerializer(AbstractHashidSerializer):
    class Meta:
        model = Message
        fields = '__all__'