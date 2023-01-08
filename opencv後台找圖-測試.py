from tkinter import W
import aircv as ac
from PIL import Image
import win32api
import win32con
import win32gui
import win32ui
import numpy as np
from ctypes import *
import cv2 as cv
from ctypes.wintypes import HWND, POINT
import time
import signal,sys
import requests
from io import BufferedReader, BytesIO
token = 'Z8NSmX4Tpz3kxW7is09KF0wVWWPUQTpLOW2hxLmKAn9' # LINE Notify 權杖


def doClick(hwnd,cx,cy):
    long_position = win32api.MAKELONG(cx, cy)#模拟鼠标指针 传送到指定坐标
    for a in range(1,10):
        print(a)
        win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)#模拟鼠标按下
        time.sleep(0.1)
        win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)#模拟鼠标弹起
# 後台截圖

def photo_capture():
    hwnd = win32gui.FindWindow(None, 'RO仙境傳說：愛如初見')  # 获取窗口的句柄
    #doClick(hwnd,600,600)
    windll.user32.SetProcessDPIAware()
    left, top, right, bot = win32gui.GetClientRect(hwnd)
    w = right - left
    h = bot - top
    hwndDC = win32gui.GetWindowDC(hwnd)  # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)  # 根据窗口的DC获取mfcDC
    saveDC = mfcDC.CreateCompatibleDC()  # mfcDC创建可兼容的DC
    saveBitMap = win32ui.CreateBitmap()  # 创建bitmap准备保存图片
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)  # 为bitmap开辟空间
    saveDC.SelectObject(saveBitMap)  # 高度saveDC，将截图保存到saveBitmap中
    # 选择合适的 window number，如0，1，2，3，直到截图从黑色变为正常画面
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 3)
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)
    #img = cv.cvtColor(np.asarray(im),cv.COLOR_BGR2GRAY)
    img = cv.cvtColor(np.asarray(im),cv.COLOR_RGB2BGR)
    #Notify("message",img)
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)
    if result == 1:
        #im.save("test.bmp")  # 调试时可打开，不保存图片可节省大量时间（约0.2s）
        return img  # 返回图片
    else:
        print("fail")
# 圖片畫圈
def draw_circle(pos, circle_radius, color, line_width, src_path):
    imsrc = src_path
    #cv.circle(imsrc, pos, circle_radius, color, line_width)
    cv.rectangle(imsrc, pos, circle_radius, color, line_width)
    cv.imshow('objDetect', imsrc)
    cv.waitKey(0)
    cv.destroyAllWindows()
# 找圖片
def find_image_cv(obj_path, src_path,x1,y1,x2,y2):
    source = crop_img(src_path,x1,y1,x2,y2) # 擷取區域圖片
    template = cv.imread(obj_path)
    result = cv.matchTemplate(source, template, cv.TM_CCOEFF_NORMED)
    pos_start = cv.minMaxLoc(result)[3]
    print( template.shape[0] , template.shape[1] )
    print( cv.minMaxLoc(result) )
    x = int(pos_start[0]) + int(template.shape[1] / 2)+x1
    y = int(pos_start[1]) + int(template.shape[0] / 2)+y1
    similarity = cv.minMaxLoc(result)[1]
    if similarity < 0.65:
        return [(-1, -1),(-1, -1),(-1, -1)]
    else:
        print("找到")
        return [(x-int(template.shape[1]/ 2)-10, y-int(template.shape[0]/ 2)-10),(x+int(template.shape[1]/ 2)+10, y+int(template.shape[0]/ 2)+10),(x,y)]
# 裁切區域
def crop_img(img,x1,y1,x2,y2):
    x_l, x_r = x1, x2  # up, down
    y_u, y_d = y1, y2  # crop image
    crop_img = img[y_u:y_d, x_l:x_r]  # notice: first y, then x
    return crop_img

def 多點找色(obj_path, src_path,x1,y1,x2,y2,sin):
    source = crop_img(src_path,x1,y1,x2,y2)
    template = cv.imread('./pic/key.bmp')
    #w,h=template.shape[::-1]
    w=template.shape[0]
    h=template.shape[1]
    res =cv.matchTemplate(template,source,cv.TM_CCOEFF_NORMED)
    loc = np.where(res >= sin)
    for pt in zip(*loc[::-1]):
        cv.rectangle(source,(pt[0]-5,pt[1]-5),(pt[0]+w+5,pt[1]+h+5),(0,255,0),2)
    cv.imshow("展示圖",source)
    cv.waitKey(1)

def term_sig_handler(signum, frame):  
    print ('catched singal: %d' % signum)
    sys.exit()

def Notify(message,image):
    headers = { "Authorization": "Bearer " + token }
    data = { 'message': message }
    ret, img_encode = cv.imencode('.jpg', image)
    str_encode = img_encode.tobytes() #將array轉化爲二進制類型
    f4 = BytesIO(str_encode) #轉化爲_io.BytesIO類型
    f4.name = '....jpg' #名稱賦值
    image = BufferedReader(f4) #轉化爲_io.BufferedReader類型
    files = { 'imageFile': image }
    print(requests.post("https://notify-api.line.me/api/notify",headers = headers, data = data, files = files))

def main1():
    signal.signal(signal.SIGTERM, term_sig_handler)  
    signal.signal(signal.SIGINT, term_sig_handler)  
    hwnd = win32gui.FindWindow(None, 'RO仙境傳說：愛如初見')  # 获取窗口的句柄
    print(hwnd)
    #circle_radius = 50
    color = (0, 255, 0)
    line_width = 3
    #src_path = photo_capture() #（當前頁面）
    obj_path = './pic/key.png' #（需要點選的地方）
    #obj_path = './pic/logs3.bmp' #（需要點選的地方）
    while 1:
        多點找色(cv.imread('./pic/key.png',0), photo_capture(),0,0,1280,720,0.65)
    #circle_center_pos,circle_radius,moveto = find_image_cv(obj_path, src_path,1097,141,1268,198)
    #draw_circle(circle_center_pos, circle_radius, color, line_width, src_path) #畫圈

if __name__ == "__main__":
    main1()