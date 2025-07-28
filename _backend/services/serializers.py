from rest_framework import serializers
from .models import ServiceRequest
from .models import Assignment

class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = '__all__'  # o lista explícita de campos que quieras exponer

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'  # O especifica los campos que quieres exponer