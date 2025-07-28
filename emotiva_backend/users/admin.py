from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Client, Collaborator, District, Document, Country, City

admin.site.site_header = "Emotiva"
admin.site.site_title = "Administración de Emotiva"
admin.site.index_title = "Panel de Administración"

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'first_name', 'last_name', 'rating', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('id',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name', 'photo', 'phone', 'rating')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    verbose_name = "Usuario"
    verbose_name_plural = "Usuarios"

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'district')
    search_fields = ('user__first_name', 'user__last_name', 'district')

@admin.register(Collaborator)
class CollaboratorAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_verified')
    search_fields = ('user__first_name', 'user__last_name')
    filter_horizontal = ('districts_coverage',)

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ("name", "city")
    search_fields = ('name',)

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('collaborator', 'document_type', 'uploaded_at')
    search_fields = ('collaborator__user__first_name', 'document_type')
    list_filter = ('document_type',)

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "country")
    list_filter = ("country",)