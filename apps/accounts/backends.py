from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class UsernameOrEmail(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        userModel=get_user_model()
        try:
            user=userModel.objects.get(username=username)
        except userModel.DoesNotExist:
            try:
                user=userModel.objects.get(email=username)
            except userModel.DoesNotExist:
                return None
        if user.check_password(password):
            return user
        return None

class Email(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        userModel=get_user_model()
        try:
            user=userModel.objects.get(email=email)
        except userModel.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None