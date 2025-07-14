from django.db.models import Q
from rest_framework import viewsets

from apps.chats.api.serializers import RoomSerializer, MessageSerializer, RoomReadSerializer
from apps.chats.models import Room, Message


class RoomViewSet(viewsets.ModelViewSet):
    model = Room
    serializer_class = RoomSerializer
    queryset = Room.objects.all()

    def get_queryset(self):
        if self.action in ["list", "retrieve"]:
            return self.request.user.rooms_as_member.all()
        return super().get_queryset()
    def get_serializer_class(self):
        if self.action == "retrieve" or self.action == "list":
            return RoomReadSerializer
        return RoomSerializer

class MessageViewSet(viewsets.ModelViewSet):
    model = Message
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

