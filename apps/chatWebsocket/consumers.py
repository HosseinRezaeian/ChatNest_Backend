import datetime

import jwt
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json

from urllib.parse import parse_qs

from itsdangerous import TimestampSigner, SignatureExpired, BadSignature

# from django.contrib.auth import get_user_model

from config import settings

from django.utils import timezone

from config.settings import TOKEN_SOCKET_SINGER





@database_sync_to_async
def save_message(sender, message, room_id):
    from apps.chats.models import Message
    return Message.objects.create(sender_id=sender, text=message, room_id_id=room_id)

@database_sync_to_async
def get_user_from_token(token):
    try:
        from django.contrib.auth import get_user_model  # ✅ اینجا import کن
        User = get_user_model()                         # ✅ اینجا صداش بزن

        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user = User.objects.get(id=payload.get("user_id"))
        return user
    except Exception:
        return None

@database_sync_to_async
def verify_token(token):
    signer = TimestampSigner(TOKEN_SOCKET_SINGER)
    try:
        from django.contrib.auth import get_user_model  # ✅ اینجا import کن
        User = get_user_model()                         # ✅ اینجا صداش بزن



        user_id = signer.unsign(token, max_age=300).decode()  # 300 ثانیه = 5 دقیقه
        return User.objects.get(id=user_id)  # اگر درست بود، ID کاربر رو برمی‌گردونه
    except SignatureExpired:
        print("توکن منقضی شده")
        return None
    except BadSignature:
        print("توکن نامعتبر یا دستکاری شده")
        return None



class chat_message(AsyncWebsocketConsumer):
    async def connect(self):
        query_string = self.scope['query_string'].decode()
        query_params = parse_qs(query_string)
        token = query_params.get('token', [None])[0]

        self.user = await verify_token(token)

        if not self.user:
            # پیام خطا بفرست به کلاینت
            await self.send_json({
                "error": "token_expired",

            })
            await self.close()
            return

        other_user_id = self.scope["url_route"]["kwargs"]["other_user_id"]
        self.room_name = other_user_id
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)


        message = data.get("message")

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "user": str(self.user.id),
                "user_email": str(self.user.email),
            }
        )

    async def chat_message(self, event):
        message = event["message"]
        user = event["user"]
        user_email = event["user_email"]
        now = timezone.now()
        await save_message(user, message, self.room_name)

        await self.send(text_data=json.dumps({
            "message": message,
            "user": user,
            "user_email": user_email,
            "time":str(now)
        }))




















# import jwt
# from channels.db import database_sync_to_async
# from channels.generic.websocket import AsyncWebsocketConsumer
# import json
#
# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import AnonymousUser
#
# from apps.chats.models import Message
# from config import settings
#
# User = get_user_model()
#
#
# @database_sync_to_async
# def get_user_from_token(token):
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
#         user = User.objects.get(id=payload.get("user_id"))
#         return user
#     except Exception:
#         return AnonymousUser()
#
#
#
#
# @database_sync_to_async
# def save_message(sender, message, room_id):
#     return Message.objects.create(sender=sender, message=message, room_id=room_id)
#
#
# class chat_message(AsyncWebsocketConsumer):
#     async def connect(self):
#         other_user_id = self.scope["url_route"]["kwargs"]["other_user_id"]
#         self.room_name = other_user_id
#         self.room_group_name = f"chat_{self.room_name}"
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#
#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         user = self.scope["user"]
#
#         print(user)
#         token = data.get("token")
#         user = await get_user_from_token(token)
#         if not user or isinstance(user, AnonymousUser):
#             await self.send(text_data=json.dumps({
#                 "error": "Unauthorized: Invalid or missing token."
#             }))
#             return
#
#         message = data.get("message")
#
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 "type": "chat_message",
#                 "message": message,
#                 "user": user,
#             }
#         )
#
#     async def chat_message(self, event):
#         message = event["message"]
#         user = event["user"]
#         await save_message(user, message, self.room_name)
#
#         await self.send(text_data=json.dumps({
#             "message": message,
#             "user": user.email,
#         }))
#
