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

class PartyMessageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartyMessage
        depth = 1
        fields = '__all__'

class PartyMessageSerializer(serializers.ModelSerializer):
    class Meta: 
        model = PartyMessage
        fields = ['content']