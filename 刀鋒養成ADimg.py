from  win32com.client import Dispatch
import time,os,json,win32gui
Path = '刀鋒'
with open("config.json", mode="r", encoding="utf-8") as file:
    config=json.load(file)
print("剩餘色偏", config["剩餘色偏"])
剩餘色偏 = config["剩餘色偏"]
print("剩餘相似度", config["剩餘相似度"])
剩餘相似度 = config["剩餘相似度"]
print("看廣告色偏", config["看廣告色偏"])
看廣告色偏 = config["看廣告色偏"]
print("看廣告相似度", config["看廣告相似度"])
看廣告相似度 = config["看廣告相似度"]
print("離開色偏", config["離開色偏"])
離開色偏 = config["離開色偏"]
print("離開相似度", config["離開相似度"])
離開相似度 = config["離開相似度"]
class Operation:
    def __init__(self):
        try:
            dm = Dispatch('dm.dmsoft')
        except Exception:
            os.system(r'regsvr32 /s %s\dm.dll' % os.getcwd())
            dm = Dispatch('dm.dmsoft')
        print("\t大漠插件版本: ",dm.Ver())
        self.dm = dm
        # self.hwnd = hwnd
        hwnd = self.dm.FindWindow("","雷電模擬器") 
        self.hwnd = self.dm.FindWindowEx(hwnd,"RenderWindow","")
        self.path = self.dm.GetBasePath()+Path
        self.dm.SetPath(self.path)
        print('\t附件路徑存放: ',self.path)
        dm_ret = self.dm.SetDict(0, "字典.txt")
        print('\t字典返回:'+ str(dm_ret)) # dm_ret類型轉換str
        print('\t窗口大小: ' + str(self.dm.GetClientSize(self.hwnd))) # 輸出窗口資訊
        dm_ret = self.dm.BindWindow(self.hwnd,'gdi','windows','windows',0)
        print('句柄:' + str(self.hwnd) + '返回:'+ str(dm_ret)) # dm_ret類型轉換str
# =================== 大漠註冊 ======================
    def 找圖(self,x1,y1,x2,y2,img,core,sin,delays):
        xy = self.dm.FindPic(x1,y1,x2,y2,img,core,sin,0)
        if xy[1] > 0:
            if delays > 0:
                print("找到 [" + img + "] "+ " X: " + str(xy[1]) + " - Y: " + str(xy[2]) + " delay: " + str(delays))
                self.dm.MoveTo(xy[1],xy[2])
                self.dm.LeftClick()
                time.sleep(delays/1000)
            return True
        else:
            return False
if __name__ == '__main__':
    # hwnd = win32gui.FindWindow(None,"雷電模擬器") 
    # hwndEx = win32gui.FindWindowEx(hwnd,None,"RenderWindow",None)
    obj = Operation() # 註冊插件
    runtime = 0
    while True:
        if obj.找圖(0, 0, 565, 90, "還剩.bmp", 剩餘色偏, 剩餘相似度, 0) == False:
            if runtime > 0:
                print('\r')
                runtime = 0
            if obj.找圖(93,260,540,902, '看廣告1.bmp|看廣告2.bmp', 看廣告色偏, 看廣告相似度, 2000) == False:
                if obj.找圖(0,0,565,450, "離.bmp|關.bmp|關閉.bmp", 離開色偏, 離開相似度, 1000) == False:
                    time.sleep(2)
        else:
            runtime += 1
            print('\r倒數中請稍後... ' + str(runtime) ,end="")
            time.sleep(1)
        # xy = dm.FindPic(0,0,2000,2000,"看廣告1.bmp|看廣告2.bmp","000000",0.7,0)
        # if xy[1] > 0:
        #     print("找到看廣告" + str(xy[1]) + "-" + str(xy[2]))
        #     dm.MoveTo(xy[1],xy[2])
        #     dm.LeftClick()
        #     time.sleep(1)
        # else:
        #     xy = dm.FindPic(0,0,2000,2000,"還剩.bmp","000000",0.55,0)
        #     if xy[1] == -1:
        #         xy = dm.FindPic(0,0,2000,2000,"離.bmp|關.bmp","000000",0.7,0)
        #         if xy[1] > 0:
        #             print("點擊關閉" + str(xy[1]) + "-" + str(xy[2]))
        #             dm.MoveTo(xy[1]+10,xy[2]+10)
        #             dm.LeftClick()
        #             time.sleep(1)
        #     else:
        #         runtime += 1
        #         print('\r倒數中請稍後... ' + str(runtime) ,end="")
        #         print("倒數中請稍後...")
        # time.sleep(1)