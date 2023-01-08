import win32gui
import win32ui
import numpy as np
from ctypes import windll
from PIL import Image
import cv2
def photo_capture():
    hwnd = win32gui.FindWindow(None, 'RO仙境傳說：愛如初見')  # 获取窗口的句柄
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
    #print(saveDC)
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 3)
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    #print(bmpstr)
    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)
    #img = np.frombuffer(bmpstr, dtype=np.uint8).reshape(im.size[1], im.size[0], 4)
    img = cv.cvtColor(np.asarray(im),cv.COLOR_RGB2BGR)
    #img=crop_img(img,994,154,1603,245)
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    if result == 1:
        # PrintWindow Succeeded
        im.save("test.bmp")  # 调试时可打开，不保存图片可节省大量时间（约0.2s）
        return img  # 返回图片
    else:
        print("fail")

def crop_img(img,x1,y1,x2,y2): # 裁切區域
    x_l, x_r = x1, x2  # up, down
    y_u, y_d = y1, y2  # crop image
    crop_img = img[y_u:y_d, x_l:x_r]  # notice: first y, then x
    return crop_img

def rotate_img(img): # 旋轉圖片 cv2.getRotationMatrix2D
    (h, w, d) = img.shape # 讀取圖片大小
    center = (w // 2, h // 2) # 找到圖片中心
    # 第一個參數旋轉中心，第二個參數旋轉角度(-順時針/+逆時針)，第三個參數縮放比例
    M = cv2.getRotationMatrix2D(center, 15, 1.0)
    # 第三個參數變化後的圖片大小
    rotate_img = cv2.warpAffine(img, M, (w, h))
    return rotate_img

def Image_CMP(Sample_img,source_img):
    hashFun = cv2.img_hash.AverageHash_create()
    Sample_hash = hashFun.compute(Sample_img)
    print (Sample_hash)
    source_hash = hashFun.compute(source_img)
    print (source_hash)
    Point = Sample_hash - source_hash
    return Point


cv2.imshow("Capture Test", photo_capture())
cv2.waitKey(0)

