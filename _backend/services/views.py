from rest_framework import generics, permissions
from .models import ServiceRequest, Assignment 
from .serializers import ServiceRequestSerializer
from .serializers import AssignmentSerializer

class ServiceRequestListCreateView(generics.ListCreateAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Asignar el usuario autenticado como cliente que crea la solicitud
        serializer.save(client=self.request.user)

class AssignmentListView(generics.ListAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]