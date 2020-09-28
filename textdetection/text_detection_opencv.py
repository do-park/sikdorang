import cv2
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import pytesseract
plt.style.use('dark_background')

img_ori = cv2.imread(r'C:\Users\multicampus\Desktop\s03p23d202\textdetection\m.jpg')
height, width, channel = img_ori.shape

plt.figure(figsize=(12, 10))
plt.imshow(img_ori, cmap='gray')