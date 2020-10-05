from rest_framework.serializers import ReadOnlyField
from rest_framework import serializers

from .models import *

class TourDetailSerializer(serializers.ModelSerializer):
    class Meta: 
        model = TripItemModel
        depth = 1
        fields = '__all__'

class GuideItemSerializer(serializers.ModelSerializer):
    # title_img = serializers.ImageField(use_url=True)
    class Meta: 
        model = TripItemModel
        fields = ['title_img', 'title', 'area', 'start_date', 'end_date', 'price', 'start_point', 'start_time', 'content', 'limit_person', 'departure_person']
    
class TourUpdateSerializer(serializers.ModelSerializer):
    # title_img = serializers.ImageField(use_url=True)
    class Meta: 
        model = TripItemModel
        fields = ['title_img', 'title', 'area', 'start_date', 'end_date', 'price', 'start_point', 'start_time', 'content', 'limit_person', 'departure_person', 'now_person']    
    
    # def update(self, instance, validated_data):
    #     instance.title_img = validated_data.get('title_img')
    #     instance.title = validated_data.get('title')
    #     instance.area = validated_data.get('area')
    #     instance.start_date = validated_data.get('start_date')
    #     instance.end_date = validated_data.get('end_date')
    #     instance.price = validated_data.get('price')
    #     instance.start_point = validated_data.get('start_point')
    #     instance.start_time = validated_data.get('start_time')
    #     instance.content = validated_data.get('content')
    #     instance.limit_person = validated_data.get('limit_person')
    #     instance.departure_person = validated_data.get('departure_person')
    #     instance.now_person = validated_data.get('now_person')
    #     instance.save()

    #     return instance

class GuideSerializer(serializers.ModelSerializer):
    class Meta: 
        model = TripItemModel
        depth = 1
        fields = ['id', 'user', 'title_img', 'title', 'area', 'start_date', 'end_date', 'price', 'start_point', 'start_time', 'limit_person', 'departure_person', 'now_person']

class TourSerializer(serializers.ModelSerializer):
    class Meta: 
        model = TripItemModel
        depth = 1
        fields = ['id', 'user', 'title_img', 'title', 'area', 'start_date', 'end_date', 'price', 'limit_person', 'departure_person', 'now_person']

class PaidSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuideTour
        fields = ['user_name', 'phone_number']