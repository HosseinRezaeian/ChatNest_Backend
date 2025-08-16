from pyexpat.errors import messages

from django.db.models import Q
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter

from apps.chats.api.serializers import MessageSerializer, PrivateRoomSerializer, PrivateRoomSerializerCreate
from apps.chats.models import Message, PrivateRoom, BaseRoom


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


class MessageViewSet(viewsets.GenericViewSet,viewsets.mixins.ListModelMixin):
    model = Message
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='room_id',
                description='Filter messages by Room ID',
                required=False,
                type=str,
                location=OpenApiParameter.QUERY
            )
        ],
        responses={200: MessageSerializer(many=True)},
        summary="List messages",

    )
    def list(self, request, *args, **kwargs):
        try:
            room_id=request.query_params.get('room_id')
            room_id = BaseRoom.objects.get(pk=room_id)
            if room_id:
                queryset = room_id.messages.all()
                self.queryset = queryset
                return super().list(request, *args, **kwargs)
        except BaseRoom.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

