from rest_framework import serializers
from .models import Notification
from services.serializers import ServiceSerializer

class NotificationSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    
    class Meta:
        model = Notification
        fields = ['id', 'service', 'message', 'is_read', 'created_at']
        read_only_fields = ['created_at']
