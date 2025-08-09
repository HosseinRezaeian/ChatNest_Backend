from itsdangerous import TimestampSigner
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings import TOKEN_SOCKET_SINGER


class SocketToken(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        signer = TimestampSigner(TOKEN_SOCKET_SINGER)
        token = signer.sign(str(request.user.id)).decode()
        return Response({'token': token},status=status.HTTP_200_OK)