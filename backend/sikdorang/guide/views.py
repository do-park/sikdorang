from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import *
from .models import *

# Create your views here.
@api_view(['POST'])
def apply_guide(request):
    User = get_user_model()
    user = get_object_or_404(User, pk=request.user.pk)
    if user.phone_number:
        user.user_code = 1
        user.save()
        return HttpResponse('가이드 획득')
    return HttpResponse('휴대폰 인증 필요')

class GuideViewSet(viewsets.ModelViewSet):
    queryset = TripItemModel.objects.all()
    serializer_class = GuideItemSerializer
    
    def create(self, data):
        print('@@@@@@@@@@@@@@@@@@@@@@@@', self.user, data.user.pk)

@api_view(['GET'])
def list_guide(request, username):
    User = get_user_model()
    user = User.objects.filter(id=username)
    trips = user.TripItemModel_set.all()
    serializer = GuideSerializer(trips, many=True)
    return Response(serializer.data)