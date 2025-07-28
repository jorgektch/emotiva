from django.contrib import admin
from .models import ServiceRequest, Assignment

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('client', 'service_type', 'quantity', 'district', 'date', 'start_time', 'duration_hours')
    list_filter = ('service_type', 'district', 'date')
    search_fields = ('client__first_name', 'client__last_name')
    date_hierarchy = 'date'
    verbose_name = "Solicitud de servicio"
    verbose_name_plural = "Solicitudes de servicio"


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('service_request', 'collaborator', 'assigned_at')
    search_fields = ('collaborator__first_name', 'collaborator__last_name', 'service_request__client__first_name')
    verbose_name = "Asignación de servicio"
    verbose_name_plural = "Asignaciones de servicio"
