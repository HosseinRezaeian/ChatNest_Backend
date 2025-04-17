from django.shortcuts import render
from    rest_framework.views import APIView
# Create your views here.


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema

class TestView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Simple Hello World API")
    def get(self, request):
        return Response({"message": "Hello World"})
