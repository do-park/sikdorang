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
    CVisit, flag = AchieveUser.objects.get_or_create(count=theme_pk, user=user, receipt=request.data['receipt'])

    # 가게 위치와 내 위치 -> 현재 theme store data에 위치 정보를 등록하지 않았다....
    
    print(CVisit.receipt)
    
    if flag:
        #이미지 경로
        image_path = CVisit.receipt
        
        #검증할 음식점 이름
        rest_name = request.data['rest_name']
        found = False
        # 결과 찾는 로직

        # 1. pytesseract만 이용했을 시
        # image = Image.open(r'C:\Users\multicampus\Desktop\s03p23d202\textdetection\screenshot.jpg')
        image = Image.open(image_path)
       
        text = pytesseract.image_to_string(image,lang='kor')

        # 결과 단어들 리스트
        results = text.replace("\n",",").replace(" ","").split(',')
        print(results)
        idx = 0
        while (not found and idx < len(results)) :
            result = results[idx]
            for i in range(len(result)-len(rest_name)+1):
                if result[i:i+len(rest_name)] == rest_name :
                    found = result[i:i+len(rest_name)]
                    print(f'방문인증 성공!!!!!!!!!! --> idx:{i}, found: {found}')
                    break
            idx += 1

        if found :
            # 성공일 때
            return HttpResponse(1)
        else :
            # 실패일 때

            # 2. opencv + pytesseract 로직

            # Read Input Image
            img_ori = cv2.imread(image_path)
            height, width, channel = img_ori.shape
            plt.figure(figsize=(12, 10))
            plt.imshow(img_ori, cmap='gray')

            # Convert Image to Grayscale
            gray = cv2.cvtColor(img_ori, cv2.COLOR_BGR2GRAY)

            plt.figure(figsize=(12, 10))
            plt.imshow(gray, cmap='gray')

            #Maximize Contrast
            structuringElement = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

            imgTopHat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, structuringElement)
            imgBlackHat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, structuringElement)

            imgGrayscalePlusTopHat = cv2.add(gray, imgTopHat)
            gray = cv2.subtract(imgGrayscalePlusTopHat, imgBlackHat)

            plt.figure(figsize=(12, 10))
            plt.imshow(gray, cmap='gray')

            # Adaptive Thresholding
            img_blurred = cv2.GaussianBlur(gray, ksize=(5, 5), sigmaX=0)

            img_thresh = cv2.adaptiveThreshold(
                img_blurred, 
                maxValue=255.0, 
                adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                thresholdType=cv2.THRESH_BINARY_INV, 
                blockSize=11, 
                C=5
            )

            plt.figure(figsize=(12, 10))
            plt.imshow(img_thresh, cmap='gray')

            # Find Contours
            contours, hierarchy = cv2.findContours(
                img_thresh, 
                mode=cv2.RETR_LIST, 
                method=cv2.CHAIN_APPROX_SIMPLE
            )

            temp_result = np.zeros((height, width, channel), dtype=np.uint8)

            cv2.drawContours(temp_result, contours=contours, contourIdx=-1, color=(255, 255, 255))

            # plt.figure(figsize=(30, 26))
            plt.figure(figsize=(12, 10))
            plt.imshow(temp_result)  

            # Prepare Data
            temp_result = np.zeros((height, width, channel), dtype=np.uint8)

            contours_dict = []

            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(temp_result, pt1=(x, y), pt2=(x+w, y+h), color=(255, 255, 255), thickness=1)
                # insert to dict
                contours_dict.append({
                    'contour': contour,
                    'x': x,
                    'y': y,
                    'w': w,
                    'h': h,
                    'cx': x + (w / 2),
                    'cy': y + (h / 2)
                })

            plt.figure(figsize=(30, 26))
            plt.imshow(temp_result, cmap='gray')  

            # Select Candidates by Char Size
            MIN_AREA = 5000
            # 가로*세로 
            MIN_WIDTH, MIN_HEIGHT = 250,50
            # 대충 가로 글자 1개당 40정도 세로 50정도
            MIN_RATIO, MAX_RATIO = 4.0, 8.0
            # 이 부분을 글자수-2, 글자수+2 정도로 변수화 하면 될 듯

            possible_contours = []

            cnt = 0
            for d in contours_dict:
                area = d['w'] * d['h']
                ratio = d['w'] / d['h']
                
                if area > MIN_AREA \
                and d['w'] > MIN_WIDTH and d['h'] > MIN_HEIGHT \
                and MIN_RATIO < ratio < MAX_RATIO:
                    d['idx'] = cnt
                    cnt += 1
                    possible_contours.append(d)
                    
            # visualize possible contours
            temp_result = np.zeros((height, width, channel), dtype=np.uint8)

            for d in possible_contours:
                final_cx = d['cx']
                final_cy = d['cy']
                cv2.rectangle(temp_result, pt1=(d['x'], d['y']), pt2=(d['x']+d['w'], d['y']+d['h']), color=(255, 255, 255), thickness=2)

            plt.figure(figsize=(12, 10))
            plt.imshow(temp_result, cmap='gray')

            # crop found letter part of total image


            # 잘려진 사진을 담을 배열, 정보 배열
            final_img = []
            final_info = []

            # 자를 사진의 가로,세로 길이
            final_w = int(MIN_WIDTH) + 4*6
            final_h = int(MIN_HEIGHT) + 5

            #자른 사진
            img_cropped = cv2.getRectSubPix(
                    img_ori, 
                    patchSize=(final_w, final_h) ,
                    center=(int(final_cx), int(final_cy))
                )
                    
                
            final_img.append(img_cropped)
            final_info.append({
                'x': int(final_cx - final_w / 2),
                'y': int(final_cy - final_h / 2),
                'w': int(final_w),
                'h': int(final_h)
            })


            plt.imshow(img_cropped, cmap='gray')

            # Another Thresholding to Find Chars
            img_result = img_cropped
    
            img_result = cv2.GaussianBlur(img_result, ksize=(3, 3), sigmaX=0)
            # _, img_result = cv2.threshold(img_result, thresh=0.0, maxval=255.0, type=cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            img_result = cv2.copyMakeBorder(img_result, top=10, bottom=10, left=10, right=10, borderType=cv2.BORDER_CONSTANT, value=(0,0,0))

            chars = pytesseract.image_to_string(img_result, lang='kor', config='--psm 7 --oem 0')

            result_chars = ''
            has_digit = False
            for c in chars:
                if ord('가') <= ord(c) <= ord('힣') or c.isdigit():
                    if c.isdigit():
                        has_digit = True
                    result_chars += c

            print(result_chars)


            plt.imshow(img_result, cmap='gray')

            # Result
            info = final_info[0]
            img_out = img_ori.copy()

            cv2.rectangle(img_out, pt1=(info['x'], info['y']), pt2=(info['x']+info['w'], info['y']+info['h']), color=(255,0,0), thickness=2)

            cv2.imwrite(result_chars + '.jpg', img_out)

            plt.figure(figsize=(12, 10))
            plt.imshow(img_out)

            print('방문한 식당 이름 : ', result_chars)

            if result_chars == rest_name:
                found = result_chars

                return HttpResponse(1)
            else: 
                return HttpResponse(-1)
        
    
 