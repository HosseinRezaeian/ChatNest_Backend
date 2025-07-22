from django.urls import path

from rest_framework.routers import DefaultRouter

from apps.chats.api.views import PrivateRoomViewSet, MessageViewSet

router_room = DefaultRouter()
router_room.register('private_rooms', PrivateRoomViewSet)

router_message = DefaultRouter()
router_message.register('Messages', MessageViewSet)


urlpatterns = [

]
urlpatterns.extend(router_room.urls)
urlpatterns.extend(router_message.urls)