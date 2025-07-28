from django.db import models
from users.models import User, Client, Collaborator

class ServiceType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class PricingRule(models.Model):
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE, related_name='pricing_rules')
    min_hours = models.PositiveIntegerField()
    max_hours = models.PositiveIntegerField()
    price_per_hour = models.DecimalField(max_digits=8, decimal_places=2)
    commission_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    
    class Meta:
        unique_together = ('service_type', 'min_hours', 'max_hours')
    
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
    people_quantity = models.PositiveIntegerField()
    date = models.DateField()
    start_time = models.TimeField()
    duration = models.PositiveIntegerField(help_text="Duración en horas")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='REQUESTED')
    address = models.TextField()
    district = models.CharField(max_length=100)
    payment_proof = models.FileField(upload_to='payment_proofs/')
    refund_proof = models.FileField(upload_to='refund_proofs/', null=True, blank=True)
    collaborator_payment_proof = models.FileField(upload_to='collaborator_payments/', null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Servicio #{self.id} - {self.get_status_display()}"

class Rating(models.Model):
    service = models.OneToOneField(Service, on_delete=models.CASCADE, related_name='rating')
    stars = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    rated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_given')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.stars} estrellas para servicio #{self.service.id}"
