import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta

DISTRICT_CHOICES = [
    ("miraflores", "Miraflores"),
    ("san_isidro", "San Isidro"),
    ("surco", "Surco"),
    ("lince", "Lince"),
    # Agrega más según sea necesario
]

SERVICE_CHOICES = [
    ("waiter", "Mozo"),
    ("bartender", "Barman"),
]

class User(AbstractUser):
    is_client = models.BooleanField('¿Es cliente?', default=False)
    is_collaborator = models.BooleanField('¿Es colaborador?', default=False)
    phone = models.CharField('Teléfono', max_length=20, blank=True)
    profile_picture = models.ImageField('Foto de perfil', upload_to='profile_pics/', blank=True, null=True)
    email_verified = models.BooleanField('Correo verificado', default=False)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.get_full_name() or self.username


class CollaboratorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='collaborator_profile')
    services_offered = models.ManyToManyField("ServiceType", verbose_name='Servicios ofrecidos')
    districts = models.ManyToManyField("District", verbose_name='Distritos de cobertura')

    class Meta:
        verbose_name = 'Perfil de colaborador'
        verbose_name_plural = 'Perfiles de colaboradores'

    def __str__(self):
        return f'Colaborador: {self.user.get_full_name()}'


class ServiceType(models.Model):
    code = models.CharField(max_length=20, choices=SERVICE_CHOICES, unique=True)
    name = models.CharField('Nombre del servicio', max_length=50)

    class Meta:
        verbose_name = 'Tipo de servicio'
        verbose_name_plural = 'Tipos de servicio'

    def __str__(self):
        return self.get_code_display()


class District(models.Model):
    code = models.CharField(max_length=30, choices=DISTRICT_CHOICES, unique=True)
    name = models.CharField('Nombre del distrito', max_length=50)

    class Meta:
        verbose_name = 'Distrito'
        verbose_name_plural = 'Distritos'

    def __str__(self):
        return self.get_code_display()

class EmailVerificationToken(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="Usuario")
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, verbose_name="Token de verificación")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        verbose_name = "Token de verificación de email"
        verbose_name_plural = "Tokens de verificación de email"

    def is_expired(self):
        # Define el token como válido por 2 días
        expiration_date = self.created_at + timedelta(days=2)
        return timezone.now() > expiration_date