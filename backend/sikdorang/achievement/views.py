from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from .serializers import *
from .models import *
from api.models import Store

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
    visited_count = [0]*150
    visited = AchieveUser.objects.filter(user=user).values()
    for i in visited:
        visited_count[i['count']] = 1
    visitchk = [theme_count, visited_count]
    return Response(visitchk)

@api_view(['POST'])
def theme_create(request, theme_pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=request.user.pk)
    CTheme, flag = ThemeUser.objects.get_or_create(count=theme_pk ,user=user)
    if flag:
        return HttpResponse('테마 클리어 등록.')
    else:
        return HttpResponse('이미 클리어된 테마입니다.')

@api_view(['POST'])
def visit_create(request, theme_pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=request.user.pk)
    CVisite, flag = AchieveUser.objects.get_or_create(count=theme_pk, user=user)

    print(f'CVisit: {CVisite}, flag : {flag}')
    # store = get_object_or_404(Store, pk=store_pk)
    # 가게 위치와 내 위치 -> 현재 theme store data에 위치 정보를 등록하지 않았다....
    # restLocation = 
    # userLocation = 

    print(f'request : {request}')
    
    if flag:
        '''
        1. 이미지 분석 -> 글자 추출 분석 & 위치 비교
        2. 이미지 분석 결과가 맞으면  -> 이미지 저장 + 방문 처리
        '''
        return HttpResponse('방문 클리어 등록.')
    else:
        return HttpResponse('이미 방문한 곳 입니다.')