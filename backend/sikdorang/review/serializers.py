from rest_framework import serializers

from .models import Review
from accounts.serializers import UserSerializer

class ReviewSerializer(serializers.ModelSerializer):
    score = serializers.IntegerField(min_value=1, max_value=5)
    class Meta: 
        model = Review
        fields = ['score', 'content']

class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'