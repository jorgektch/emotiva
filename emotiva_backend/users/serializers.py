from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Client, Collaborator, District, Document

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'photo', 'rating']
        extra_kwargs = {'password': {'write_only': True}}

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        
        if hasattr(user, 'client'):
            token['role'] = 'client'
        elif hasattr(user, 'collaborator'):
            token['role'] = 'collaborator'
        else:
            token['role'] = 'admin'
        
        return token

class ClientRegisterSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Client
        fields = ['user', 'address', 'district']
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        client = Client.objects.create(user=user, **validated_data)
        return client

class CollaboratorRegisterSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    districts = serializers.PrimaryKeyRelatedField(
        queryset=District.objects.all(),
        many=True,
        source='districts_coverage',
        required=False
    )
    
    class Meta:
        model = Collaborator
        fields = ['user', 'districts']
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        districts = validated_data.pop('districts_coverage', [])
        user = User.objects.create_user(**user_data)
        collaborator = Collaborator.objects.create(user=user)
        collaborator.districts_coverage.set(districts)
        return collaborator

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'document_type', 'file', 'uploaded_at']
        read_only_fields = ['uploaded_at']

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'name']
