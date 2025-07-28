from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .models import Client, Collaborator, Document
from .serializers import (
    UserSerializer, CustomTokenObtainPairSerializer, 
    ClientRegisterSerializer, CollaboratorRegisterSerializer,
    DocumentSerializer
)

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class ClientRegisterView(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientRegisterSerializer
    permission_classes = [permissions.AllowAny]

class CollaboratorRegisterView(generics.CreateAPIView):
    queryset = Collaborator.objects.all()
    serializer_class = CollaboratorRegisterSerializer
    permission_classes = [permissions.AllowAny]

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user

class DocumentUploadView(generics.CreateAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        collaborator = self.request.user.collaborator
        serializer.save(collaborator=collaborator)

class DocumentListView(generics.ListAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Document.objects.filter(collaborator=self.request.user.collaborator)
