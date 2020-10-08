from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import *
from .models import Review
from api.models import Store, TagModel
from rest_framework import status
from konlpy.tag import Komoran

# Create your views here.

@api_view(['POST'])
def create_review(request, store_pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=request.user.pk)
    store = get_object_or_404(Store, pk=store_pk)
    
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=user, store_id=store)
        if request.data["score"] > 6:
            TAG_NAME = ["가성비", "청결", "친절", "분위기", "인테리어", "아침", "점심", "저녁", "친구", "연인", "가족", "주차장"]
            tag_dict = {"가성비":0,"저렴":0,"깔끔":1,"신선":1,"위생":1,"깨끗":1,"친절":2,"분위기":3,"감성":3,"인테리어":4,"아침":5,"조식":5,"새벽":5,"점심시간":6,"점심":6,"낮":6,"퇴근":7,"석식":7,"술":7,"야식":7,"밤":7,"저녁":7,"친구":8,"연인":9,"데이트":9,"둘이서":9,"여자친구":9,"여친":9,"남자친구":9,"남친":9,"커플":9,"가족":10,"부모님":10,"주차장":11,"주차공간":11,"주차권":11}
            
            km = Komoran()
            nouns = []
            try:
                nouns = km.nouns(request.data['content'])
                print(nouns)
            except:
                pass
            tags = set()
            for noun in nouns:
                if noun in tag_dict.keys():
                    tags.add(tag_dict[noun])
            if tags:
                stag = list(tags)
                for i in stag:
                    utag = TagModel.objects.filter(user=user, name=str(i))
                    if utag.exists():
                        utag2 = TagModel.objects.get(user=user, name=str(i))
                        utag2.count += 1
                        print(utag2.count)
                        utag2.save()
                    else:
                        TagModel.objects.create(user=user, name=str(i), count=1)
 
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(data=serializer.errors)

@api_view(['GET'])
def user_review(request):
    User = get_user_model()
    user = get_object_or_404(User, pk=request.user.pk)
    reviews = Review.objects.filter(user=user.pk).order_by('-created_at')
    serializer = ReviewListSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def store_review(request, store_pk):
    reviews = Review.objects.filter(store_id=store_pk)
    serializer = ReviewListSerializer(reviews, many=True)
    return Response(serializer.data)

# @api_view(['GET'])
# def review_chk(request, store_pk):
#     User = get_user_model()
#     user = get_object_or_404(User, pk=request.user.pk)
#     review = Review.objects.filter(user=user, store_id=store_pk)
#     if review.exists():
#         return HttpResponse('1')
#     else:
#         return HttpResponse('0')