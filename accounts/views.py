from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import OtpSendSerializer, OtpRegisterSerializer
from .models import OtpList, CustomUser
import datetime
from rest_framework import status

from datetime import timedelta
from django.utils import timezone
import random
from rest_framework_simplejwt.tokens import RefreshToken

class SendOtp(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    serializer_class = OtpSendSerializer

    def post(self, request):
        print(request.data)
        uv = OtpSendSerializer(data=request.data)

        if uv.is_valid():
            sender_phone = request.data.get('phone_number')
            print('OTP is valid')
            random_number = 0
            opt_serach = OtpList.objects.filter(phone_number=sender_phone).first()
            if not opt_serach:
                user = CustomUser.objects.filter(phone_number=sender_phone)
                random_number = random.randint(10000, 99999)
                otp_create = OtpList(phone_number=sender_phone, otp_token=str(random_number),
                                     datetime=datetime.datetime.now() + timedelta(minutes=1),
                                     account=user[0] if len(user) > 0 else None)
                otp_create.save()
            else:
                random_number = random.randint(10000, 99999)

                opt_serach.otp_token = str(random_number)
                opt_serach.datetime = datetime.datetime.now() + timedelta(minutes=1)
                opt_serach.save()

            return Response({"status": "ok", "message": f"OTP sent successfully", 'token': str(random_number)})
        else:
            # Print validation errors
            print(uv.errors)
            return Response({"status": "error", "errors": uv.errors}, status=400)


class RegisterOtp(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = OtpRegisterSerializer

    def post(self, request):
        print(request.data)
        uv = OtpRegisterSerializer(data=request.data)
        if uv.is_valid():
            sender_phone = request.data.get('phone_number')
            sender_token = request.data.get('token')
            print('OTP is valid')
            opt_serach = OtpList.objects.filter(phone_number=sender_phone, otp_token=sender_token)

            if not opt_serach:
                return Response({"status": "error", "errors": 'cant find this'}, status=400)
            if opt_serach[0].datetime < timezone.now():
                return Response({"status": "error", "errors": 'time is finsh'}, status=400)
            if opt_serach[0].account == None:
                user = CustomUser(phone_number=sender_phone,is_staff=True)
                user.save()
            user=opt_serach[0].account
            tokens = self.get_tokens_for_user(user)
            opt_serach.delete()
            return Response(tokens, status=status.HTTP_200_OK)



    @staticmethod
    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
