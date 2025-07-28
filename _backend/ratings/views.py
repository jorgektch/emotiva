# ratings/views.py

from rest_framework import generics, permissions
from .models import Rating
from .serializers import RatingSerializer

class RatingListCreateView(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]  # o permisos que prefieras
