from rest_framework import serializers
from rest_framework.serializers import ReadOnlyField

from .models import Trip
from accounts.serializers import UserSerializer

class TripListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'

class TripSerializer(serializers.ModelSerializer):
    trip_user = ReadOnlyField(source='user.id')
    class Meta: 
        model = Trip
        fields = ['trip_user','name', 'plan', 'date']
