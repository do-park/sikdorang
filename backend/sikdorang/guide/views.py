from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, authentication_classes
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework.response import Response
# from rest_framework import viewsets
from .serializers import *
from .models import *
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import status
import datetime


# Create your views here.

@api_view(['POST'])
def create_tour(request):
    User = get_user_model()
    user = get_object_or_404(User, pk=request.user.pk)
    print('!!!!!!!!!!!!', request.data)
    serializer = GuideItemSerializer(data=request.data)
    print('@@@@@@@@', serializer)
    if serializer.is_valid():
        serializer.save(user=user)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(data=serializer.errors)

@api_view(['GET'])
def list_tour(request):
    now = datetime.datetime.now()
    nowDate = now.strftime('%Y%m%d')
    tours = TripItemModel.objects.filter(start_date__gte=int(nowDate)).order_by('-start_date')
    serializer = TourSerializer(tours, many=True)
    return Response(serializer.data)

# class GuideViewSet(viewsets.ModelViewSet):
#     queryset = TripItemModel.objects.all()
#     serializer_class = GuideItemSerializer
#     def perform_create(self, serializer):
#         serializer.save(user_id=self.request.user.pk)

@api_view(['GET'])
def detail_tour(request, tour_pk):
    tour = TripItemModel.objects.filter(pk=tour_pk)
    serializer = TourDetailSerializer(tour, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def list_guide(request, username):
    User = get_user_model()
    user = User.objects.filter(id=username)
    trips = user.TripItemModel_set.all()
    serializer = GuideSerializer(trips, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def paid(request, trip_pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=request.user.pk)
    trip = get_object_or_404(TripItemModel, pk=trip_pk)
    tour = GuideTour.objects.filter(user=user)
    if tour.exists():
        return HttpResponse('이미 결제된 여행입니다.')
    else:
        GuideTour.objects.create(user=user, trip_item=trip, user_name=request.data['user_name'], phone_number=request.data['phone_number'])
        return HttpResponse('결제 되었습니다.')

@api_view(['GET'])
def paidtour(request):
    User = get_user_model()
    user = get_object_or_404(User, pk=request.user.pk)
    tours = user.TripItemModel_set.all()
    serializer = TourSerializer(tours, many=True)
    return Response(serializer.data)