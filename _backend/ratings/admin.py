from django.contrib import admin
from .models import Rating

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('rated_user', 'rated_by', 'service', 'score', 'created_at')
    list_filter = ('score',)
    search_fields = ('rated_user__username', 'rated_by__username')
    verbose_name = "Calificación"
    verbose_name_plural = "Calificaciones"
