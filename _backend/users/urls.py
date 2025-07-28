from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('verify-email/<uuid:token>/', views.VerifyEmailView.as_view(), name='verify_email'),

    # Más rutas como login/logout, perfil colaborador, etc. se pueden agregar aquí.
]
