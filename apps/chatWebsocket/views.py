from rest_framework.views import APIView
from rest_framework.response import Response

class MyAPI(APIView):
    def get(self, request):
        return Response({"message": "Hello from DRF!"})
