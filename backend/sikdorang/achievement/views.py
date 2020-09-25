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

@api_view(['GET'])
def theme_clear(request):
    User = get_user_model()
    user = get_object_or_404(User, pk=request.user.pk)
    theme_count = [0]*12
    themes = ThemeUser.objects.filter(user=user).values()
    print(themes)
    for i in themes:
        theme_count[i['count']] = 1
    return Response(theme_count)

@api_view(['POST'])
def theme_create(request, theme_pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=request.user.pk)
    CTheme, flag = ThemeUser.objects.get_or_create(count=theme_pk ,user=user)
    if flag:
        return HttpResponse('테마 클리어 등록.')
    else:
        return HttpResponse('이미 클리어된 테마입니다.')

@api_view(['GET'])
def visited(request, theme_pk):
    astores = AchiveStore.objects.filter(theme=theme_pk)
    serializer = AStoreListSerializer(astores, many=True)
    return Response(serializer.data)