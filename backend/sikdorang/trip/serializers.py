from rest_framework import serializers

from .models import Trip
from accounts.serializers import UserSerializer

class TripListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'

class TripSerializer(serializers.ModelSerializer):
    # user = UserSerializer(required=False)  # required=False => is_valid() 에서 유무검증 pass
    class Meta: 
        model = Trip
        fields = '__all__'
