import cv2
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import pytesseract
import os 
import configparser
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
plt.style.use('dark_background')



config = configparser.ConfigParser()
config.read(os.path.dirname(os.path.realpath(__file__)) + os.sep + 'envs' + os.sep + 'property.ini')

# 이미지 -> 문자열 추출
# def ocrToStr(fullPath, outTxtPath, fileName, lang='eng') :
#     img = Image.open(fullPath)
#     txtName = os.path.join(outTxtPath,fileName.split('.')[0])

#     outText = image_to_string(img, lang=lang, config="--psm 1 -c preserve_interword_spaces=1")
    

#     print("+++ OCT EXTRACT RESERT +++")
#     print("EXTRACT FILENAME ->>> : ", fileName, ' : <<<-')
#     print('\n\n')

#     print(outText)
#     strToTxt(txtName,outText)

def ocrToStr(fullPath, fileName, lang='eng') :
    img = Image.open(fullPath)
    outText = pytesseract.image_to_string(img, lang=lang)
    print("+++ OCT EXTRACT RESERT +++")
    print("EXTRACT FILENAME ->>> : ", fileName, ' : <<<-')
    print('\n\n')

    print(outText)
    strToTxt(fileName,outText)

def strToTxt(txtName, outText):
    with open(txtName + '.txt', 'w', encoding='utf-8') as f:
        f.write(outText)

if __name__ == "__main__":
    # outTxtPath = os.path.dirname(os.path.realpath(__file__))+config['path']['OcrTxtPath']

    # for root, dirs, files in os.walk(os.path.dirname(os.path.realpath(__file__))+config['path']['OriImgPath']):
    #     for fname in files:
    #         fullName = os.path.join(root,fname)
    #         ocrToStr(fullName, outTxtPath, fname, 'kor+eng')
    fullPath = r'C:\Users\multicampus\Desktop\s03p23d202\textdetection\mo1.jpg'


    # ocrToStr(fullPath, '결과', 'kor+eng')
    ocrToStr(fullPath, '결과', 'kor')
