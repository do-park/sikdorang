from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import *
from .models import Review
from api.models import Store
from rest_framework import status
# Create your views here.

@api_view(['POST'])
def create_review(request, store_pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=request.user.pk)
    store = get_object_or_404(Store, pk=store_pk)
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=user, store_id=store)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(data=serializer.errors)

@api_view(['GET'])
def user_review(request):
    User = get_user_model()
    user = get_object_or_404(User, pk=request.user.pk)
    reviews = Review.objects.filter(user=user.pk)
    serializer = ReviewListSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def store_review(request, store_pk):
    reviews = Review.objects.filter(store_id=store_pk)
    serializer = ReviewListSerializer(reviews, many=True)
    return Response(serializer.data)