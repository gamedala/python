import win32com.client
import time
import datetime
dm = win32com.client.Dispatch('dm.dmsoft')

Path = '愛如初見'
print('插件版本:'+dm.ver()) # 顯是插件版本
base_path = dm.GetBasePath() + Path # 取得插件路徑
dm_ret = dm.SetPath(base_path) # 設定全局路徑
print('路徑:' + base_path) # dm_ret類型轉換str
dm_ret = dm.SetDict(0, "字典.txt")
print('返回:'+ str(dm_ret)) # dm_ret類型轉換str
hwnd = dm.FindWindow("","雷電模擬器") 
hwndEx = dm.FindWindowEx(hwnd,"RenderWindow","")
dm_ret = dm.BindWindow(hwndEx,'gdi','windows','windows',0)
print('句柄:' + str(hwndEx) + '返回:'+ str(dm_ret)) # dm_ret類型轉換str

def 找圖(x1,y1,x2,y2,img,sin,delays):
    xy = dm.FindPic(x1,y1,x2,y2,img,"000000",sin,0)
    x=xy[1]
    y=xy[2]
    if x > 0:
        now=datetime.datetime.now()
        print(str(now) +" "+ img + " X: " + str(x) + " - Y: " + str(y) + " delay: " + str(delays))
        dm.MoveTo(x,y)
        dm.LeftClick()
        time.sleep(delays/1000)
        return True
    else:
        #time.sleep(1)
        return False

def Unix(now1):
    now2 = int(time.time())
    renow = now2 - now1
    return renow


while True:
    if 找圖( 71, 149, 1205, 548, "愛如初見APP.bmp", 0.9, 5000) == True :
        star=int(time.time())
        print("*** 180秒登入未成功清除APP重新登入 ***")
        while True:
            找圖(609, 624, 669, 653, "好喔.bmp", 0.9, 5000)
            找圖(609, 455, 670, 488, "確認.bmp", 0.9, 5000)
            找圖(574, 600, 705, 638, "進入遊戲.bmp", 0.9, 5000)
            找圖(1059, 652, 1166, 686, "開始遊戲.bmp", 0.9, 5000)
            if 找圖(98, 66, 130, 90, "確認登入.bmp", 0.8, 0) == True:
                while 找圖(953,279,1037,301, "全部魔物.bmp", 0.8, 2000) == False:
                    找圖(1147,199,1194,216, "全自動.bmp", 0.8, 2000)

                print("登入完成!\n持續每5秒偵測是否初先APP圖示")
                break
            if Unix(star) > 180:
                dm.KeyPress(113)
                time.sleep(3)
                找圖(891, 72, 978, 96, "全部清除.bmp", 0.9, 5000)
                break
    else:
        time.sleep(5)