from rest_framework import serializers
from .models import DriverMatch

class DriverMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverMatch
        fields = ['driver', 'criteria', 'matched_at']
