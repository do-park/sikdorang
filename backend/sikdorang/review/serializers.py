from rest_framework import serializers

from .models import Review
from accounts.serializers import UserSerializer

class ReviewSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Review
        fields = '__all__'
