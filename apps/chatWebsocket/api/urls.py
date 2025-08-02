from django.urls import path

from apps.chatWebsocket.api.view import SocketToken

urlpatterns = [

path("token/",SocketToken.as_view(),name="socketoken"),
]


