from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, CollaboratorProfile, ServiceType, District

# Configuración del sitio admin
admin.site.site_header = "Emotiva"
admin.site.site_title = "Panel de administración"
admin.site.index_title = "Bienvenido al panel de administración de Emotiva"

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_client', 'is_collaborator', 'email_verified')
    list_filter = ('is_client', 'is_collaborator', 'email_verified', 'is_active')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Información adicional', {
            'fields': ('phone', 'profile_picture', 'is_client', 'is_collaborator', 'email_verified'),
        }),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('id',)
    verbose_name = "Usuario"
    verbose_name_plural = "Usuarios"


@admin.register(CollaboratorProfile)
class CollaboratorProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    filter_horizontal = ('services_offered', 'districts')
    search_fields = ('user__first_name', 'user__last_name')
    verbose_name = "Perfil de colaborador"
    verbose_name_plural = "Perfiles de colaboradores"


@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    verbose_name = "Tipo de servicio"
    verbose_name_plural = "Tipos de servicio"


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    verbose_name = "Distrito"
    verbose_name_plural = "Distritos"
