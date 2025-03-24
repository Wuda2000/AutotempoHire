from rest_framework import serializers
from .models import Post, Trip

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'created_at', 'updated_at']

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ['trip_id', 'car_owner', 'driver', 'pickup_location', 'destination', 'departure_time', 'arrival_time', 'trip_date', 'status', 'price', 'created_at']
