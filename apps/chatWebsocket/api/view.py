from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from itsdangerous import TimestampSigner, BadSignature, SignatureExpired


class SocketToken(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        signer = TimestampSigner('your-secret-key')
        token = signer.sign(f'user_id:{request.user.id}').decode()
        print(token)
        return Response({'token': token},status=status.HTTP_200_OK)