from rest_framework import serializers

from .models import AchiveStore

class AStoreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AchiveStore
        fields = '__all__'