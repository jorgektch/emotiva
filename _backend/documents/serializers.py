# documents/serializers.py

from rest_framework import serializers
from .models import BackgroundCheck

class BackgroundCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackgroundCheck
        fields = '__all__'  # O especifica los campos que necesites
