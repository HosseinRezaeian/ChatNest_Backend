from rest_framework import viewsets

from apps.chats.api.serializers import RoomSerializer, MessageSerializer
from apps.chats.models import Room, Message


class RoomViewSet(viewsets.ModelViewSet):
    model = Room
    serializer_class = RoomSerializer
    queryset = Room.objects.all()

class MessageViewSet(viewsets.ModelViewSet):
    model = Message
    serializer_class = MessageSerializer
    queryset = Message.objects.all()