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

def ocrToStr(fullPath, fileName, lang='eng') :
    img = Image.open(fullPath)
    outText = pytesseract.image_to_string(img, lang=lang)
    print(outText.replace(" ",""))

    # strToTxt(fileName,outText)

def strToTxt(txtName, outText):
    with open(txtName + '.txt', 'w', encoding='utf-8') as f:
        f.write(outText)

if __name__ == "__main__":
 
    fullPath = r'C:\Users\multicampus\Desktop\s03p23d202\textdetection\sinhan.jpg'


    ocrToStr(fullPath, '결과', 'kor')
