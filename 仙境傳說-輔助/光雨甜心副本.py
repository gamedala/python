import ctypes, sys
from  win32com.client import Dispatch
import time,os,win32gui
Path = '光雨'

class Operation:
    def __init__(self):
        try:
            self.dm = Dispatch('dm.dmsoft')
        except Exception:
            os.system(r'regsvr32 /s %s\dm.dll' % os.getcwd())
            self.dm = Dispatch('dm.dmsoft')
        print("\t大漠插件版本: ",self.dm.Ver())
        self.hwnd = win32gui.FindWindow(None,"Ragnarok")
        self.path = self.dm.GetBasePath()+Path
        self.dm.SetPath(self.path)
        print('\t附件路徑存放: ',self.path)
        dm_ret = self.dm.SetDict(0, "關鍵字.txt")
        print('\t字典返回:'+ str(dm_ret)) # dm_ret類型轉換str
        dm_ret = self.dm.BindWindow(self.hwnd,'gdi','dx2','dx',4)
        if dm_ret == 1:
            print('\t綁定成功')
        else:
            print(' 綁定失敗')
            quit()
            
    def 按鍵(self,KEY_ID):
        self.dm.keydown(KEY_ID)
        self.dm.keyup(KEY_ID)

    def 記憶體字串(self,位置):
        return self.dm.ReadString(self.hwnd, 位置, 0, 15)
    
    def 記憶體數值(self,位置):
        return self.dm.ReadInt(self.hwnd, 位置, 0)

if __name__ == '__main__':
   job = Operation() # 註冊插件
   地圖 = now_地圖 = ""
   按下 = 進入副本 = 0
   while True: # 迴圈
       地圖 = job.記憶體字串("011513C0")
       if now_地圖 != 地圖: # 宣告地圖
           now_地圖 = 地圖
           print(now_地圖)
       
       if now_地圖 == "ba_maison": # 當在副本入口時
           if job.記憶體數值("00F05990") > 0 : # 有對話窗口
               xy = job.dm.FindStr(76,423,131,609, "副本關閉", "000000-000000", 0.95) # 有沒有出現副本關閉窗口
               if xy[1] > -1:
                   job.按鍵(40)
                   進入副本 = 1
               job.按鍵(13)
               time.sleep(0.5)
               按下 = 按下 +1
           elif 按下 > 0:
               xy = job.dm.FindStr(232, 206, 599, 463, "捕獲甜心", "000000-000000", 1.0) # 尋找副本NPC
               if xy[1] > -1:
                   job.dm.MoveTo(xy[1]+40,xy[2]+60)
                   job.dm.LeftClick()
           else:
               xy = job.dm.FindStr(7,720,117,733, "目中的副本", "b5ffb5-000000", 1.0) # 已經重置時間
               if xy[1] > -1:
                   按下 = 按下 +1
               else:
                   job.按鍵(120)
                   time.sleep(0.2)
       elif now_地圖 == "1@bamq": # 當在副本時
           if 進入副本 == 1:
               time.sleep(1)
               進入副本 = 0
           Now_X = job.記憶體數值("0113EA34")
           Now_Y = job.記憶體數值("0113EA38")
           if  Now_X <= 32 :
               job.dm.MoveTo(511, 378)
               job.dm.LeftDown()
               job.dm.MoveTo(807, 389)
               time.sleep(0.2)
           elif Now_X >= 36:
               job.dm.Leftup()
               time.sleep(0.5)
               找NPC = True
               while 找NPC == True:
                   if job.記憶體數值("00F05998"):
                       xy = job.dm.FindStr(131, 89, 882, 600, "的心", "000000-000000", 1.0)
                       if xy[1] > -1:
                           job.按鍵(40)
                       job.按鍵(13)
                   elif job.記憶體數值("00F05990"):
                       job.按鍵(13)
                   else:
                       xy = job.dm.FindColor(371, 193, 968, 517, "ffff55-000000", 1.0, 0)
                       if xy[1] > -1:
                           job.dm.MoveTo(xy[1],xy[2])
                           job.dm.LeftClick()
                   if job.記憶體字串("011513C0") != "1@bamq":
                       找NPC = False
       else: # 當不再任何腳本地圖時
           time.sleep(1)
           xy = job.dm.FindStr(76,423,131,609, "副本關閉", "000000-000000", 0.95)
           if xy[1] > -1:
               job.dm.MoveTo(xy[1],xy[2])
               job.dm.LeftClick()
               按下 = 0
               time.sleep(0.5)
           else:
               job.dm.MoveTo(858,93)
               job.dm.LeftClick()
               if job.記憶體數值("00F05998"):
                   job.按鍵(40)
                   job.按鍵(13)
                   time.sleep(0.2)
                   for i in range(0,27):
                       job.按鍵(40)
                   time.sleep(0.5)
                   job.按鍵(13)
                   time.sleep(0.5)
                   job.按鍵(13)
                   time.sleep(0.5)
                   for i in range(0,13):
                       job.按鍵(40)
                   for i in range(0,3):
                       job.按鍵(13)
                       time.sleep(0.3)
       time.sleep(0.05)