import win32com.client
import time
dm = win32com.client.Dispatch('dm.dmsoft')

print('插件版本:'+dm.ver()) # 顯是插件版本
hwnd = dm.FindWindow("","League of Legends")
hwnd = dm.FindWindowEx(hwnd,"CefBrowserWindow","")
hwnd = dm.FindWindowEx(hwnd,"Chrome_WidgetWin_0","")
#hwnd = dm.FindWindowEx(hwnd,"","Chrome Legacy Window")
dm_ret = dm.BindWindow(hwnd,'gdi','dx2','windows',4)
print('句柄:' + str(hwnd) + '返回:'+ str(dm_ret)) # dm_ret類型轉換str

第幾個 = 1

if hwnd > 0:
    #while True:
        dm.MoveTo(1100,200+(第幾個*50))
        dm.LeftDown()
        for i in range(1,15):
            dm.MoveTo(1100-(i*10),200+(第幾個*50)-(i*5))
            time.sleep(0.001)
        time.sleep(0.5)
        dm.LeftUp()
        time.sleep(0.1)