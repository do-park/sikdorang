from PIL import Image
import pytesseract
import cv2
import numpy as np
import matplotlib.pyplot as plt
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

rest_name = '리안중화요리'

# 결과 찾는 로직

# 1. pytesseract만 이용했을 시
image = Image.open(r'C:\Users\multicampus\Desktop\s03p23d202\textdetection\screenshot.jpg')
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

# 만약 pytesseract만 해서 결과값이 나온다면 opencv사용하지 않고 종료          
if found :
    print(f'{found} 음식점의 방문 인증이 완료되었습니다.')

# 결과값이 나오지 않았다면 opencv사용
else :
