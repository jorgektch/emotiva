from django.db import models
from users.models import User
from services.models import ServiceRequest

class Rating(models.Model):
    rated_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_ratings', verbose_name='Usuario calificado')
    rated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_ratings', verbose_name='Calificado por')
    service = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, verbose_name='Servicio')
    score = models.DecimalField('Puntaje', max_digits=2, decimal_places=1)
    comment = models.TextField('Comentario', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Calificación'
        verbose_name_plural = 'Calificaciones'

    def __str__(self):
        return f'{self.rated_user} calificado con {self.score}'
