from django.contrib import admin
from django.utils.html import format_html
from .models import ServiceType, PricingRule, Service, Rating

@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon_preview', 'photo1_preview', 'photo2_preview', 'photo3_preview']
    readonly_fields = ['icon_preview', 'photo1_preview', 'photo2_preview', 'photo3_preview']
    fieldsets = (
        (None, {
            'fields': ('name', 'description')
        }),
        ("Ícono", {
            'fields': ('icon', 'icon_preview'),
        }),
        ("Fotos", {
            'fields': ('photo1', 'photo1_preview', 'photo2', 'photo2_preview', 'photo3', 'photo3_preview'),
        }),
    )

    def icon_preview(self, obj):
        if obj.icon:
            return format_html('<img src="{}" style="height: 50px;" />', obj.icon.url)
        return "(Sin ícono)"
    icon_preview.short_description = "Ícono"

    def photo1_preview(self, obj):
        if obj.photo1:
            return format_html('<img src="{}" style="height: 50px;" />', obj.photo1.url)
        return "(Sin foto)"
    photo1_preview.short_description = "Foto 1"

    def photo2_preview(self, obj):
        if obj.photo2:
            return format_html('<img src="{}" style="height: 50px;" />', obj.photo2.url)
        return "(Sin foto)"
    photo2_preview.short_description = "Foto 2"

    def photo3_preview(self, obj):
        if obj.photo3:
            return format_html('<img src="{}" style="height: 50px;" />', obj.photo3.url)
        return "(Sin foto)"
    photo3_preview.short_description = "Foto 3"

@admin.register(PricingRule)
class PricingRuleAdmin(admin.ModelAdmin):
    list_display = ('service_type', 'min_hours', 'max_hours', 'price_per_hour', 'commission_percentage')
    list_filter = ('service_type',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'service_type', 'date', 'start_time', 'status')
    list_filter = ('status', 'date', 'service_type')
    search_fields = ('client__user__first_name', 'collaborator__user__first_name', 'district')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('service', 'stars', 'rated_by', 'created_at')
    list_filter = ('stars',)
