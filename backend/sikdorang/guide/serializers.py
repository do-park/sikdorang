from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import *

class GuideItemSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta: 
        model = TripItemModel
        fields = '__all__'
        
    def create(self, data):
        print('@@@@@@@@@@@@@@@@@@@@@@@@', self.__dict__, data.user.pk)

class GuideSerializer(serializers.ModelSerializer):
    
    class Meta: 
        model = TripItemModel
        fields = ['user', 'title_img', 'title', 'area', 'start_date', 'end_date', 'price', 'start_point', 'start_time']