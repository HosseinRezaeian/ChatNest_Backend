from django.contrib.auth import get_user_model
from django.shortcuts import render
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.contacts.api.serializer import ContactSerializer
from apps.contacts.models import Contact

User = get_user_model()
# Create your views here.



class ContactView(GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ContactSerializer

    def get_queryset(self):
        return Contact.objects.filter(source=self.request.user)

    @action(detail=False, methods=["get"], url_path="get_contact")
    def get_contacts(self, request):
        user = self.request.user
        contacts = Contact.objects.filter(source=user)
        return Response(ContactSerializer(contacts, many=True).data)

    @extend_schema(
        request=ContactSerializer,
        responses={200: None},
        methods=["POST"],
        parameters=[
            OpenApiParameter(name='search', type=str, location=OpenApiParameter.QUERY)
        ]
    )
    @action(detail=False, methods=["post"], url_path="add_contact")
    def add_contact(self, request):
        user = self.request.user
        search = request.query_params.get("search")
        search_contact=User.objects.filter(email=search).first()
        if not search_contact:
            raise ValidationError({"detail": "not found"})

        if user.id == search_contact.id:
            raise ValidationError({"detail": "you cant add your self in contacts"})

        contacts = Contact.objects.create(source=user,target=search_contact)
        return Response(ContactSerializer(contacts).data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Contact deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, *args, **kwargs):

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)