from  win32com.client import Dispatch
import time,os,json,win32gui
Path = '刀鋒'
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
        dm_ret = self.dm.SetDict(0, "字典.txt")
        print('\t字典返回:'+ str(dm_ret)) # dm_ret類型轉換str
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
if __name__ == '__main__':
    obj = Operation() # 註冊插件
    runtime = 0
    while True:
        if obj.找字(0, 25, 720, 50, "還剩", "646364-656465", 0.75, (0,0), 0) == False and obj.找字(0, 25, 720, 50, "還剩", "D3D4D5-2C2B2A", 0.75, (0,0), 0) == False:
            if runtime > 0:
                print('\r')
                runtime = 0
            if obj.找字(0,25,720,60, "關|離", "646364-656465", 0.82, (10,10), 1000) == False and obj.找字(650,400,680,560, "關|離", "646364-656465", 0.82, (10,10), 1000) == False:
                if obj.找字(0,25,720,60, "閉|離", "fafafa-151515", 0.8, (10,10), 1000) == False and obj.找字(650,400,680,560, "閉|離", "fafafa-151515", 0.8, (10,10), 1000) == False:
                    if obj.找字(50,300,680,1150, '看廣告', 'E3E6E9-212121|6E481A-271A0B', 0.75, (20,10), 2000) == False:
                        time.sleep(2)
        else:
            runtime += 1
            print('\r倒數中請稍後... ' + str(runtime) ,end="")
            # print('\r'+time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime())+" 倒數中請稍後... " + str(runtime) ,end="")
            time.sleep(1)