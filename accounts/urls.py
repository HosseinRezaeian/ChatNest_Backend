from django.urls import path
from .views import SendOtp,RegisterOtp
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('send-otp/', SendOtp.as_view(), name='send_otp'),
    path('register-otp/', RegisterOtp.as_view(), name='register_otp'),
]
