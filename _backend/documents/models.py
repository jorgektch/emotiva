from django.db import models
from users.models import User

class BackgroundCheck(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='background_documents')
    police_clearance = models.FileField('Certificado policial', upload_to='documents/', blank=True, null=True)
    criminal_clearance = models.FileField('Certificado penal', upload_to='documents/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Documento de antecedentes'
        verbose_name_plural = 'Documentos de antecedentes'

    def __str__(self):
        return f'Antecedentes de {self.user}'
