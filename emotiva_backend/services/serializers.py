from rest_framework import serializers
from .models import ServiceType, PricingRule, Service, Rating
from users.serializers import UserSerializer

class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = ['id', 'name', 'description']

class PricingRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingRule
        fields = ['id', 'service_type', 'min_hours', 'max_hours', 'price_per_hour', 'commission_percentage']

class ServiceSerializer(serializers.ModelSerializer):
    client = UserSerializer(read_only=True)
    collaborator = UserSerializer(read_only=True)
    
    class Meta:
        model = Service
        fields = [
            'id', 'client', 'collaborator', 'service_type', 'people_quantity', 
            'date', 'start_time', 'duration', 'status', 'address', 'district',
            'total_price', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'total_price']

class ServiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            'service_type', 'people_quantity', 'date', 'start_time', 
            'duration', 'address', 'district', 'payment_proof'
        ]

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'service', 'stars', 'comment', 'rated_by', 'created_at']
        read_only_fields = ['rated_by', 'created_at']
