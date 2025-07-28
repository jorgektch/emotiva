from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .models import BackgroundCheck
from .serializers import BackgroundCheckSerializer

class BackgroundCheckUploadView(generics.CreateAPIView):
    queryset = BackgroundCheck.objects.all()
    serializer_class = BackgroundCheckSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MyDocumentsView(generics.ListAPIView):
    serializer_class = BackgroundCheckSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Solo devuelve documentos del usuario autenticado
        return BackgroundCheck.objects.filter(user=self.request.user)