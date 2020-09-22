from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from .serializers import *
from .models import *

# Create your views here.
@api_view(['GET'])
def astore_list(request, theme_pk):
    astores = AchiveStore.objects.filter(theme=theme_pk)
    serializer = AStoreListSerializer(astores, many=True)
    return Response(serializer.data)
