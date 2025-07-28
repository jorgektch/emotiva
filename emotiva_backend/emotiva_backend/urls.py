"""
URL configuration for emotiva_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import (
    CustomTokenObtainPairView,
    ClientRegisterView,
    CollaboratorRegisterView,
    UserProfileView,
    DocumentUploadView,
    DocumentListView
)
from services.views import (
    ServiceTypeListView,
    PricingRuleListView,
    ServiceCreateView,
    ServiceListView,
    ServiceDetailView,
    RatingCreateView
)
from notifications.views import NotificationListView, MarkAsReadView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Autenticación
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Usuarios
    path('api/register/client/', ClientRegisterView.as_view(), name='register_client'),
    path('api/register/collaborator/', CollaboratorRegisterView.as_view(), name='register_collaborator'),
    path('api/profile/', UserProfileView.as_view(), name='user_profile'),
    path('api/documents/', DocumentListView.as_view(), name='document_list'),
    path('api/documents/upload/', DocumentUploadView.as_view(), name='document_upload'),
    
    # Servicios
    path('api/service-types/', ServiceTypeListView.as_view(), name='service_type_list'),
    path('api/pricing-rules/', PricingRuleListView.as_view(), name='pricing_rule_list'),
    path('api/services/', ServiceListView.as_view(), name='service_list'),
    path('api/services/create/', ServiceCreateView.as_view(), name='service_create'),
    path('api/services/<int:pk>/', ServiceDetailView.as_view(), name='service_detail'),
    path('api/ratings/', RatingCreateView.as_view(), name='rating_create'),
    
    # Notificaciones
    path('api/notifications/', NotificationListView.as_view(), name='notification_list'),
    path('api/notifications/<int:pk>/mark-as-read/', MarkAsReadView.as_view(), name='mark_as_read'),
]