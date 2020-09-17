from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import Trip

from rest_framework import viewsets

# Create your views here.
@api_view(['GET'])
def trip_list(request, user_pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=user_pk)
    trips = user.trip_set.all()
    serializer = TripListSerializer(trips, many=True)
    return Response(serializer.data)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def create_trip(request):
#     serializer = TripSerializer(data=request.data)
#     if serializer.is_valid(raise_exception=True):
#         serializer.save(user=request.user)
#         return Response(serializer.data)

# @api_view(['GET'])
# def trip_detail(request, trip_pk):
#     trip = get_object_or_404(Trip, pk=trip_pk)
#     serializer = TripSerializer(trip)
#     return Response(serializer.data)

class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
