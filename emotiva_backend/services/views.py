from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q
from .models import Service, ServiceType, PricingRule, Rating
from .serializers import (
    ServiceSerializer, ServiceCreateSerializer,
    ServiceTypeSerializer, PricingRuleSerializer,
    RatingSerializer
)
from users.models import Collaborator
from notifications.models import Notification

class ServiceTypeListView(generics.ListAPIView):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer
    permission_classes = [permissions.AllowAny]

class PricingRuleListView(generics.ListAPIView):
    queryset = PricingRule.objects.all()
    serializer_class = PricingRuleSerializer
    permission_classes = [permissions.AllowAny]

class ServiceCreateView(generics.CreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        client = self.request.user.client
        serializer.save(client=client, status='REQUESTED')

class ServiceListView(generics.ListAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'client'):
            return Service.objects.filter(client=user.client).order_by('-created_at')
        elif hasattr(user, 'collaborator'):
            return Service.objects.filter(
                Q(collaborator=user.collaborator) | 
                Q(status='REQUESTED', 
                  district__in=user.collaborator.districts_coverage.all(),
                  service_type__in=user.collaborator.services.all())
            ).order_by('-created_at')
        return Service.objects.none()

class ServiceDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'client'):
            return Service.objects.filter(client=user.client)
        elif hasattr(user, 'collaborator'):
            return Service.objects.filter(
                Q(collaborator=user.collaborator) | 
                Q(status='REQUESTED', 
                  district__in=user.collaborator.districts_coverage.all(),
                  service_type__in=user.collaborator.services.all())
            )
        return Service.objects.none()
    
    def perform_update(self, serializer):
        instance = self.get_object()
        user = self.request.user
        new_status = serializer.validated_data.get('status', instance.status)
        
        # Lógica para cambios de estado
        if new_status != instance.status:
            if new_status == 'ASSIGNED' and hasattr(user, 'collaborator'):
                serializer.save(collaborator=user.collaborator)
                
                # Notificar al cliente
                Notification.objects.create(
                    user=instance.client.user,
                    service=instance,
                    message=f"Tu servicio ha sido asignado a {user.get_full_name()}"
                )
            else:
                serializer.save()
                
                # Notificar al otro usuario
                if hasattr(user, 'client'):
                    if instance.collaborator:
                        Notification.objects.create(
                            user=instance.collaborator.user,
                            service=instance,
                            message=f"El cliente ha cambiado el estado del servicio a {new_status}"
                        )
                elif hasattr(user, 'collaborator'):
                    Notification.objects.create(
                        user=instance.client.user,
                        service=instance,
                        message=f"El colaborador ha cambiado el estado del servicio a {new_status}"
                    )
        else:
            serializer.save()

class RatingCreateView(generics.CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        service = serializer.validated_data['service']
        if service.status != 'COMPLETED':
            raise serializers.ValidationError("Solo se puede calificar servicios completados")
        
        # Verificar que el usuario es cliente o colaborador del servicio
        user = self.request.user
        if not (hasattr(user, 'client') and user.client == service.client) and \
           not (hasattr(user, 'collaborator') and user.collaborator == service.collaborator):
            raise serializers.ValidationError("No tienes permiso para calificar este servicio")
        
        serializer.save(rated_by=user)
        
        # Actualizar rating del usuario calificado
        if hasattr(user, 'client'):
            # Cliente calificando al colaborador
            collaborator = service.collaborator.user
            ratings = Rating.objects.filter(service__collaborator=service.collaborator)
            avg_rating = ratings.aggregate(models.Avg('stars'))['stars__avg']
            collaborator.rating = avg_rating
            collaborator.save()
        else:
            # Colaborador calificando al cliente
            client = service.client.user
            ratings = Rating.objects.filter(service__client=service.client)
            avg_rating = ratings.aggregate(models.Avg('stars'))['stars__avg']
            client.rating = avg_rating
            client.save()
