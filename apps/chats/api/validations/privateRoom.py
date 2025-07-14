
from  rest_framework import serializers

from apps.chats.models import Room


def validatePrivateRoom(data):
    if data['type'] == 'private':
        members = data.get('members', [])
        if len(members) > 2:
            raise serializers.ValidationError("Private room must have exactly 2 members.")

        user_ids = set(member.id for member in members)
        existing_rooms = Room.objects.filter(type='private')
        for room in existing_rooms:
            room_member_ids = set(room.members.values_list('id', flat=True))
            if room_member_ids == user_ids:
                raise serializers.ValidationError("A private room with these members already exists.")

    return data