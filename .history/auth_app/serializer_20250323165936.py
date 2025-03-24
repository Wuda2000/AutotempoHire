from rest_framework import serializers
from .models import CustomUser, DriverApplication

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['unique_id', 'username', 'email', 'role', 'is_active']

class DriverApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverApplication
        fields = ['user', 'first_name', 'surname', 'age', 'ethnicity', 'years_of_experience', 'kcse_certificate', 'good_conduct', 'cover_letter', 'cv', 'status', 'applied_at']
