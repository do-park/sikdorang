from rest_framework import serializers
from rest_framework.serializers import ReadOnlyField

from .models import *

class PartyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        depth = 1
        fields = '__all__'

class PartySerializer(serializers.ModelSerializer):
    class Meta: 
        model = Party
        fields = ['title', 'trip_date', 'content']
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title')
        instance.trip_date = validated_data.get('trip_date')
        instance.content = validated_data.get('content')
        instance.save()

        return instance

class PartyMessageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartyMessage
        depth = 1
        fields = '__all__'

class PartyMessageSerializer(serializers.ModelSerializer):
    class Meta: 
        model = PartyMessage
        fields = ['content']