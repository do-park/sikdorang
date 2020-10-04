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
        fields = ['title_img', 'title', 'area', 'start_date', 'end_date', 'price', 'start_point', 'start_time', 'content', 'limit_person', 'departure_person', 'now_person']

class GuideSerializer(serializers.ModelSerializer):
    class Meta: 
        model = TripItemModel
        depth = 1
        fields = ['id', 'user', 'title_img', 'title', 'area', 'start_date', 'end_date', 'price', 'start_point', 'start_time', 'limit_person', 'departure_person', 'now_person']

class TourSerializer(serializers.ModelSerializer):
    class Meta: 
        model = TripItemModel
        depth = 1
        fields = ['user', 'title_img', 'title', 'area', 'start_date', 'end_date', 'price', 'limit_person', 'departure_person', 'now_person']

class PaidSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuideTour
        fields = ['user_name', 'phone_number']
