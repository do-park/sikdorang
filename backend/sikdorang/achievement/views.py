from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from .serializers import *
from .models import *
from api.models import Store
from PIL import Image
import pytesseract
import cv2
import numpy as np
import matplotlib.pyplot as plt
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


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
    # rest_name = request.data['rest_name']
    # visit_image = request.data['visit_image']
    # print(f'rest_name : {rest_name}')
    # print(f'visit_image : {visit_image}')
    print(CVisite.receipt)
    
    if flag:
        #이미지 경로
        # image_path = request.data['visit_image']
        image_path = r'C:\Users\multicampus\Desktop\s03p23d202\textdetection\phone_bill.jpg'
        
        #검증할 음식점 이름
        rest_name = request.data['rest_name']
        found = False
        # 결과 찾는 로직

        # 1. pytesseract만 이용했을 시
        # image = Image.open(r'C:\Users\multicampus\Desktop\s03p23d202\textdetection\screenshot.jpg')
        image = Image.open(image_path)
        # print(image)
        text = pytesseract.image_to_string(image,lang='kor')

        # 결과 단어들 리스트
        results = text.replace("\n",",").replace(" ","").split(',')
        print(results)

        for result in results :
            for i in range(len(result)-len(rest_name)):
                if result[i:i+len(rest_name)] == rest_name :
                    found = result[i:i+len(rest_name)]
                    print(f'idx:{i}, found: {found}')
                    break
        return HttpResponse('방문 클리어 등록.')

        # if not found :
        #     img_ori = cv2.imread(image_path)

        #     height, width, channel = img_ori.shape
        #     #Convert Image to Grayscale
        #     gray = cv2.cvtColor(img_ori, cv2.COLOR_BGR2GRAY)

        # return HttpResponse('방문 클리어 등록.')
    else:
        return HttpResponse('이미 방문한 곳 입니다.')