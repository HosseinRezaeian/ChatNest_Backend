import jwt
from urllib.parse import parse_qs
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

User = get_user_model()

@database_sync_to_async
def get_user_from_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user = User.objects.get(id=payload.get("user_id"))
        return user
    except Exception:
        return AnonymousUser()

class JwtAuthMiddleware(BaseMiddleware):
    def populate_scope(self, scope):
        if "user" not in scope:
            scope["user"] = AnonymousUser()

    async def resolve_scope(self, scope):
        # فرض بر این است که توکن JWT از query string ارسال می‌شود
        query_string = scope.get("query_string", b"").decode()
        params = parse_qs(query_string)
        token_list = params.get("token", None)

        if token_list:
            token = token_list[0]
            user = await get_user_from_token(token)
        else:
            user = AnonymousUser()

        scope["user"] = user

    async def __call__(self, scope, receive, send):
        scope = dict(scope)
        self.populate_scope(scope)
        await self.resolve_scope(scope)
        return await super().__call__(scope, receive, send)

