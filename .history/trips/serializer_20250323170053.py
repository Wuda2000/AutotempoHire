from rest_framework import serializers
from .models import Post, Trip

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'created_at', 'updated_at']

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
