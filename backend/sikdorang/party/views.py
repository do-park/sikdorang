from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework.response import Response
# from rest_framework import viewsets
from .serializers import *
from .models import *
from trip.models import Trip
from rest_framework import status

# Create your views here.

@api_view(['POST'])
def create_party(request, trip_pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=request.user.pk)
    trip = get_object_or_404(Trip, pk=trip_pk)
    serializer = PartySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=user, trip_id = trip)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(data=serializer.errors)

@api_view(['GET'])
def list_party(request):
    parties = Party.objects.all()
    serializer = PartyListSerializer(parties, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def detail_party(request, party_pk):
    party = Party.objects.filter(pk=party_pk)
    serializer = PartyListSerializer(party, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
def update_party(request, party_pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=request.user.pk)
    party = get_object_or_404(Party, pk=party_pk)
    if party.user == user:
        serializer = PartySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user, trip_id=party.trip_id)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        
    return HttpResponse('Something Wrong')

@api_view(['DELETE'])
def delete_party(request, party_pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=request.user.pk)
    party = get_object_or_404(Party, id=party_pk)
    if party.user == user:
        party.delete()
        return HttpResponse('잘 지워짐')
    return HttpResponse('니 글 아님 ㅅㄱ')

@api_view(['POST'])
def create_message(request, party_pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=request.user.pk)
    party = get_object_or_404(Party, pk=party_pk)
    serializer = PartyMessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=user, party_id = party)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(data=serializer.errors)

@api_view(['GET'])
def list_message(request, party_pk):
    messages = PartyMessage.objects.filter(pk=party_pk)
    serializer = PartyMessageListSerializer(messages, many=True)
    return Response(serializer.data)