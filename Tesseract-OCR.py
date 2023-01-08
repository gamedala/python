from PIL import Image
import pytesseract
import cv2
import numpy as np
#image = Image.open('./pic/logs.bmp')
#print(pytesseract.image_to_string(image, lang='chi_tra')) 

#content = pyte
# sseract.image_to_string(image)   # 识别图片
#print(content)
#pytesseract.pytesseract,tesseract_cmd = "C:/Program Files/Tesseract-OCR/tessdata.exe"

def zh_ch(string):
    return string.encode("big5").decode('UTF-8', errors='ignore')


testdata_dir_config = '--tessdata-dir "C:/Program Files/Tesseract-OCR/tessdata"'
path = "./pic/logs.bmp"
openimg = Image.open(path)
img = cv2.imread(path)
img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

#textCode = pytesseract.image_to_string(openimg,config=testdata_dir_config,lang='chi_tra')
hImg,WImg,_=img.shape
boxes=pytesseract.image_to_boxes(img,config=testdata_dir_config,lang='chi_tra')
for b in boxes.splitlines():
    #print(b)
    b=b.split(' ')
    x,y,w,h=int(b[1]),int(b[2]),int(b[3]),int(b[4])
    cv2.rectangle(img,(x,y),(w,h),(0,255,0),2)
    print(b[0])
    cv2.putText(img,b[0],(x,hImg-y+25),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
cv2.imshow("imgshow",img)
cv2.waitKey(0)