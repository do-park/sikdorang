from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, authentication_classes
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
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
    serializer = GuideItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=user)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(data=serializer.errors)

@api_view(['GET'])
def list_tour(request):
    now = datetime.datetime.now()
    nowDate = now.strftime('%Y%m%d')
    tours = TripItemModel.objects.filter(start_date__gte=int(nowDate)).order_by('start_date')
    serializer = TourSerializer(tours, many=True)
    return Response(serializer.data)

# class GuideViewSet(viewsets.ModelViewSet):
#     queryset = TripItemModel.objects.all()
#     serializer_class = GuideItemSerializer
#     def perform_create(self, serializer):
#         serializer.save(user_id=self.request.user.pk)

@api_view(['GET'])
def detail_tour(request, tour_pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=request.user.pk)
    tours = TripItemModel.objects.filter(pk=tour_pk)[0]
    paiders = GuideTour.objects.filter(trip_item=tour_pk)
    flag = False
    for paider in paiders:
        if paider.user == user:
            flag = True
    serializer = TourDetailSerializer(tours)
    return JsonResponse({"result": serializer.data, "flag": flag})
 

@api_view(['GET'])
def list_guide(request):
    User = get_user_model()
    user = get_object_or_404(User, pk=request.user.pk)
    now = datetime.datetime.now()
    nowDate = now.strftime('%Y%m%d')
    trips = TripItemModel.objects.filter(start_date__gte=int(nowDate), user=user).order_by('start_date')
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
        trip.now_person += 1
        trip.save()
        return HttpResponse('결제 되었습니다.')

@api_view(['GET'])
def paidtour(request):
    User = get_user_model()
    user = get_object_or_404(User, pk=request.user.pk)
    tours = GuideTour.objects.filter(user=user)
    serializer = PaidSerializer(tours, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def paider(request, trip_pk):
    paider = GuideTour.objects.filter(trip_item=trip_pk)
    serializer = PaidSerializer(paider, many=True)
    return Response(serializer.data)

# @api_view(['PUT'])
# def update_guide(request, trip_pk):
#     User = get_user_model()
#     user = get_object_or_404(User, pk=request.user.pk)
#     tour = get_object_or_404(TripItemModel, pk=trip_pk)
#     if tour.user == user:
#         serializer = GuideItemSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.update(tour, request.data)
#             return Response(serializer.data)
        
#     return HttpResponse('Something Wrong')

@api_view(['DELETE'])
def delete_tour(request, tour_pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=request.user.pk)
    tour = get_object_or_404(TripItemModel, pk=tour_pk)
    
    if tour.user == user:
        paider = GuideTour.objects.filter(trip_item=tour_pk)
        if paider  :
            return Response('이미 결제한 사람 있어서 삭제 불가',  status=status.HTTP_400_BAD_REQUEST)
        else :
            tour.delete()
            return HttpResponse('잘 지워짐')
    return Response('니 글 아님 ㅅㄱ', status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_tour(request, tour_pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=request.user.pk)
    tour = get_object_or_404(TripItemModel, pk=tour_pk)
    if tour.user == user:
        serializer = TourUpdateSerializer(tour, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
    return HttpResponse('Something Wrong')