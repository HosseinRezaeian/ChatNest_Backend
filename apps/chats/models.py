from django.db import models
from django.conf import settings

TYPE_ROOM = [
    ('private', 'Private'),
    ('group', 'Group'),
    ('channel', 'Channel')]


class Room(models.Model):
    name = models.CharField(max_length=60)
    type = models.CharField(max_length=40, choices=TYPE_ROOM)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='UserRoom', through_fields=("room", "user"))


class UserRoom(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    class Meta:
        db_table = "user_room"


class Message(models.Model):
    text = models.CharField(max_length=255)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    create_time = models.DateTimeField(auto_now_add=True)
