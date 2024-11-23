from rest_framework import serializers
from django.core.validators import RegexValidator


class OtpSendSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=12,
                                         validators=[
                                             RegexValidator(
                                                 regex=r'^09\d{9}$',
                                                 message="Phone number must start with '09' and be 11 digits long.",
                                                 code='invalid_phone_number'
                                             )
                                         ])


class OtpRegisterSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=12,
                                         validators=[
                                             RegexValidator(
                                                 regex=r'^09\d{9}$',
                                                 message="Phone number must start with '09' and be 11 digits long.",
                                                 code='invalid_phone_number'
                                             )
                                         ])
    token = serializers.CharField(max_length=10,
                                  validators=[
                                      RegexValidator(
                                          regex=r'^\d+$',
                                          message="Phone number must start with '09' and be 11 digits long.",
                                          code='invalid_phone_number'
                                      )
                                  ])
