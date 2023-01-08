from  win32com.client import Dispatch
import time,os,json,win32gui
Path = '史萊姆傳奇'
token = 'Z8NSmX4Tpz3kxW7is09KF0wVWWPUQTpLOW2hxLmKAn9' # LINE Notify 權杖
class Operation:
    def __init__(self):
        try:
            self.dm = Dispatch('dm.dmsoft')
        except Exception:
            os.system(r'regsvr32 /s %s\dm.dll' % os.getcwd())
            self.dm = Dispatch('dm.dmsoft')
        print("\t大漠插件版本: ",self.dm.Ver())
        self.hwndEX = win32gui.FindWindow(None,"雷電模擬器") 
        self.hwnd = win32gui.FindWindowEx(self.hwndEX,None,"RenderWindow",None)
        self.path = self.dm.GetBasePath()+Path
        self.dm.SetPath(self.path)
        print('\t附件路徑存放: ',self.path)
        # dm_ret = self.dm.SetDict(0, "字典.txt")
        # print('\t字典返回:'+ str(dm_ret)) # dm_ret類型轉換str
        self.dm.SetShowErrorMsg(0)
        self.Bind()

    def Bind(self):
        #self.dm.SetClientSize(self.hwnd, 1280, 720) # 設定窗口大小
        window = self.dm.GetClientSize(self.hwnd)
        if window[1] != 720 & window[2] != 1280 :
            self.dm.SetClientSize(self.hwndEX, 761,1315) # 設定窗口大小
        print('\t窗口大小: ' + str(self.dm.GetClientSize(self.hwnd))) # 輸出窗口資訊
        dm_ret = self.dm.BindWindow(self.hwnd,'gdi','windows','windows',0)
        if dm_ret == 1:
            print('\t綁定成功')
        else:
            print(' 綁定失敗')
# =================== 大漠註冊 ======================
    def 找字(self,x1,y1,x2,y2,ocr,core,sin,偏差,delays):
        xy = self.dm.FindStr(x1,y1,x2,y2,ocr,core,sin)
        if xy[1] > 0:
            if delays > 0:
                print("找到 [" + ocr + "] "+ " X: " + str(xy[1]) + " - Y: " + str(xy[2]) + " 偏差X: " + str(偏差[0]) + " - 偏差Y: " + str(偏差[1]) + " delay: " + str(delays))
                time.sleep(0.5)
                self.dm.MoveTo(xy[1]+偏差[0],xy[2]+偏差[1])
                self.dm.LeftClick()
                time.sleep(delays/1000)
            return True
        else:
            return False
    def 找圖(self,x1,y1,x2,y2,pic,core,sin,方向,偏差,delays):
        xy = self.dm.FindPic(x1,y1,x2,y2,pic,core,sin,方向)
        if xy[1] > 0:
            if delays > 0:
                print("找到 [" + pic + "] "+ " X: " + str(xy[1]) + " - Y: " + str(xy[2]) + " 偏差X: " + str(偏差[0]) + " - 偏差Y: " + str(偏差[1]) + " delay: " + str(delays))
                time.sleep(0.5)
                self.dm.MoveTo(xy[1]+偏差[0],xy[2]+偏差[1])
                self.dm.LeftClick()
                time.sleep(delays/1000)
            return True
        else:
            return False
if __name__ == '__main__':
    obj = Operation() # 註冊插件
    
    while True:
        obj.找圖(86,656,627,697, "領取.bmp", "050505", 0.6, 0, (30,30), 1)

        time.sleep(1)