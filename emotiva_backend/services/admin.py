from django.contrib import admin
from .models import ServiceType, PricingRule, Service, Rating

@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

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
