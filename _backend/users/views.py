from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import RegisterSerializer, ProfileSerializer
from .models import User

class RegisterView(APIView):
    """
    Vista para registrar nuevos usuarios (colaboradores o clientes)
    """

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Registro exitoso. Revisa tu correo para activar tu cuenta."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    """
    Vista para obtener y actualizar el perfil del usuario autenticado
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    """
    Activa la cuenta del usuario mediante un token enviado por correo
    """

    def get(self, request, token):
        # Buscar el token de verificación
        verification_token = get_object_or_404(EmailVerificationToken, token=token)

        if verification_token.is_expired():
            return Response({"detail": "El token ha expirado."}, status=status.HTTP_400_BAD_REQUEST)

        user = verification_token.user
        user.is_active = True
        user.email_verified = True  # Si tienes este campo
        user.save()

        # Opcional: eliminar token después de uso
        verification_token.delete()

        return Response({"message": "Cuenta activada correctamente."}, status=status.HTTP_200_OK)
