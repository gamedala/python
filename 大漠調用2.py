import win32com.client
import time
dm = win32com.client.Dispatch('dm.dmsoft')

def setDM():
    Path = '刀鋒'
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

setDM

while True:
    xy = dm.FindPic(0,0,2000,2000,"看廣告1.bmp|看廣告2.bmp","000000",0.7,0)
    if xy[1] > 0:
        print("找到看廣告" + str(xy[1]) + "-" + str(xy[2]))
        dm.MoveTo(xy[1],xy[2])
        dm.LeftClick()
        time.sleep(1)
    else:
        xy = dm.FindPic(0,0,2000,2000,"還剩.bmp","000000",0.55,0)
        if xy[1] == -1:
            xy = dm.FindPic(0,0,2000,2000,"離.bmp|關.bmp","000000",0.7,0)
            if xy[1] > 0:
                print("點擊關閉" + str(xy[1]) + "-" + str(xy[2]))
                dm.MoveTo(xy[1]+10,xy[2]+10)
                dm.LeftClick()
                time.sleep(1)
        else:
            print("倒數中請稍後...")
    time.sleep(1)