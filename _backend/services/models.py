from django.db import models
from users.models import User, ServiceType, District
from django.utils import timezone

class ServiceRequest(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='service_requests')
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE, verbose_name='Tipo de servicio')
    quantity = models.PositiveIntegerField('Cantidad requerida')
    district = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name='Distrito del servicio')
    date = models.DateField('Fecha del servicio')
    start_time = models.TimeField('Hora de inicio')
    duration_hours = models.DecimalField('Duración (horas)', max_digits=4, decimal_places=2)
    comments = models.TextField('Comentarios adicionales', blank=True)

    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Solicitud de servicio'
        verbose_name_plural = 'Solicitudes de servicio'

    def __str__(self):
        return f'Servicio de {self.service_type} para {self.client.get_full_name()}'

class Assignment(models.Model):
    service_request = models.OneToOneField(ServiceRequest, on_delete=models.CASCADE, verbose_name='Solicitud')
    collaborator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments', verbose_name='Colaborador')
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Asignación de servicio'
        verbose_name_plural = 'Asignaciones de servicio'

    def __str__(self):
        return f'{self.collaborator.get_full_name()} asignado a {self.service_request}'
