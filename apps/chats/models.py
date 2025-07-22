from django.db import models
from django.conf import settings

from utils.abstract.models import AbstractCreateUpdateModel, AbstractCreator, AbstractHashId



class BaseRoom(AbstractHashId, AbstractCreateUpdateModel, AbstractCreator):
    name = models.CharField(max_length=60)


class PrivateRoom(BaseRoom):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='private_rooms_as_user1')
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='private_rooms_as_user2')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user1', 'user2'], name='unique_private_room')
        ]

    def save(self, *args, **kwargs):
        if self.user1.id > self.user2.id:
            self.user1, self.user2 = self.user2, self.user1
        super().save(*args, **kwargs)


class Message(AbstractHashId, AbstractCreateUpdateModel):
    text = models.CharField(max_length=255)
    room_id = models.ForeignKey(BaseRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
