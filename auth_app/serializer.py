from rest_framework import serializers
from .models import CustomUser, DriverApplication

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'is_active']

class DriverApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverApplication
        fields = ['id', 'user', 'first_name', 'surname', 'age', 'ethnicity', 'years_of_experience', 'status', 'applied_at']
