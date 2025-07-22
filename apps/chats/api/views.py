from django.db.models import Q
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse

from apps.chats.api.serializers import MessageSerializer, PrivateRoomSerializer, PrivateRoomSerializerCreate
from apps.chats.models import  Message,PrivateRoom


class PrivateRoomViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    model = PrivateRoom
    serializer_class = PrivateRoomSerializer
    queryset = PrivateRoom.objects.all()

    def get_queryset(self):
        if self.action in ["list", "retrieve"]:
            user = self.request.user
            return PrivateRoom.objects.filter(Q(user1=user) | Q(user2=user))

        return super().get_queryset()
    def get_serializer_class(self):
        return PrivateRoomSerializer

    @extend_schema(
        request=PrivateRoomSerializerCreate,
        responses={
            200: PrivateRoomSerializer,
            400: OpenApiResponse(description="Invalid input data")
        },
    )
    @action(detail=False, methods=["post"], url_path="create-or-get")
    def create_or_get_room(self, request):
        serializer = PrivateRoomSerializerCreate(data=request.data,context={'request': request})
        if serializer.is_valid():
            room = serializer.save()
            return Response(PrivateRoomSerializer(room).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageViewSet(viewsets.ModelViewSet):
    model = Message
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

