from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
image = Image.open(r'C:\Users\multicampus\Desktop\s03p23d202\textdetection\rian1.jpg')
# path1 = os.path.normpath("my_path/this_way")
text = pytesseract.image_to_string(image,lang='kor')
print(text)
print(text.replace(" ",""))