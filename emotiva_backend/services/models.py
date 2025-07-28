from django.db import models
from users.models import User, Client, Collaborator, District

class ServiceType(models.Model):
    name = models.CharField("Nombre", max_length=50, unique=True)
    description = models.TextField("Descripción", blank=True)
    icon = models.ImageField("Ícono (PNG)", upload_to='service_icons/', null=True, blank=True)

    photo1 = models.ImageField("Foto 1", upload_to='service_photos/', null=True, blank=True)
    photo2 = models.ImageField("Foto 2", upload_to='service_photos/', null=True, blank=True)
    photo3 = models.ImageField("Foto 3", upload_to='service_photos/', null=True, blank=True)

    class Meta:
        verbose_name = "Tipo de Servicio"
        verbose_name_plural = "Tipos de Servicios"

    def __str__(self):
        return self.name

class PricingRule(models.Model):
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE, related_name='pricing_rules')
    min_hours = models.PositiveIntegerField("Horas mínimas")
    max_hours = models.PositiveIntegerField("Horas máximas")
    price_per_hour = models.DecimalField("Precio por hora", max_digits=8, decimal_places=2)
    commission_percentage = models.DecimalField("Porcentaje de comisión", max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ('service_type', 'min_hours', 'max_hours')
        verbose_name = "Regla de precio"
        verbose_name_plural = "Reglas de precio"

    def __str__(self):
        return f"{self.service_type.name}: {self.min_hours}-{self.max_hours} horas - S/{self.price_per_hour}"

class Service(models.Model):
    STATUS_CHOICES = (
        ('REQUESTED', 'Solicitado'),
        ('ASSIGNED', 'Asignado'),
        ('ON_ROUTE', 'En camino'),
        ('IN_PROGRESS', 'En curso'),
        ('COMPLETED', 'Finalizado'),
        ('CANCELLED', 'Cancelado'),
    )

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='services')
    collaborator = models.ForeignKey(Collaborator, on_delete=models.SET_NULL, null=True, blank=True, related_name='services')
    service_type = models.ForeignKey(ServiceType, on_delete=models.PROTECT)
    people_quantity = models.PositiveIntegerField("Cantidad de personas")
    date = models.DateField("Fecha")
    start_time = models.TimeField("Hora de inicio")
    duration = models.PositiveIntegerField("Duración en horas", help_text="Duración en horas")
    status = models.CharField("Estado", max_length=20, choices=STATUS_CHOICES, default='REQUESTED')
    address = models.TextField("Dirección")
    district = models.ForeignKey(District, on_delete=models.PROTECT, related_name='services', verbose_name="Distrito")

    latitude = models.DecimalField("Latitud", max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField("Longitud", max_digits=9, decimal_places=6, null=True, blank=True)

    payment_proof = models.FileField("Comprobante de pago", upload_to='payment_proofs/')
    refund_proof = models.FileField("Comprobante de reembolso", upload_to='refund_proofs/', null=True, blank=True)
    collaborator_payment_proof = models.FileField("Comprobante de pago al colaborador", upload_to='collaborator_payments/', null=True, blank=True)

    total_price = models.DecimalField("Precio total", max_digits=10, decimal_places=2, null=True, blank=True)

    created_at = models.DateTimeField("Creado el", auto_now_add=True)
    updated_at = models.DateTimeField("Actualizado el", auto_now=True)

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"

    def __str__(self):
        return f"Servicio #{self.id} - {self.get_status_display()}"

class Rating(models.Model):
    service = models.OneToOneField(Service, on_delete=models.CASCADE, related_name='rating')
    stars = models.PositiveSmallIntegerField("Estrellas", choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField("Comentario", blank=True)
    rated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_given')
    created_at = models.DateTimeField("Creado el", auto_now_add=True)

    class Meta:
        verbose_name = "Calificación"
        verbose_name_plural = "Calificaciones"

    def __str__(self):
        return f"{self.stars} estrellas para servicio #{self.service.id}"
