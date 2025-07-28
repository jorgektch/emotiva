from django.contrib import admin
from .models import BackgroundCheck

@admin.register(BackgroundCheck)
class BackgroundCheckAdmin(admin.ModelAdmin):
    list_display = ('user', 'uploaded_at')
    search_fields = ('user__username', 'user__email')
    verbose_name = "Documento de antecedentes"
    verbose_name_plural = "Documentos de antecedentes"
