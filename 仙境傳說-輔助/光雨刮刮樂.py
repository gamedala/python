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
        dm_ret = self.dm.SetDict(0, "驗證.txt")
        print('\t字典返回:'+ str(dm_ret)) # dm_ret類型轉換str
        dm_ret = self.dm.BindWindow(self.hwnd,'gdi','dx2','dx',4)
        if dm_ret == 1:
            print('\t綁定成功')
        else:
            print(' 綁定失敗')
            
def Unix(set_now):
    now = int(time.time()*1000)
    renow = set_now - now
    return renow

def 秒(set_now):
    now = int(time.time())
    renow = int(set_now/1000) - now
    return renow
def 轉換日期(Unix):
    time_local = time.localtime(Unix/1000)
    # 转换成新的时间格式(精确到秒)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return dt
if __name__ == '__main__':
    job = Operation() # 註冊插件
    冷卻時間 = 0
    使用時間 = 0
    倒數時間 = 0
    while True:
        if Unix(冷卻時間) <= 30000 and Unix(使用時間) <= 0 :
            job.dm.keydown(112)
            job.dm.keyup(112)
            使用時間 = int(time.time()*1000) + 1003
            print('使用冷卻毫秒',Unix(使用時間))
            time.sleep(0.1)
            msg = job.dm.Ocr(240, 707, 265, 720, "b5ffb5-000000", 0.9)
            if msg != "" :
                if int(msg) > 0 :
                    冷卻時間 = int(time.time()*1000) + ( int(msg) * 60000 )
                    到期時間 = 轉換日期(冷卻時間)
                    print('找到冷卻分鐘',msg,'冷卻毫秒',Unix(冷卻時間))
        冷卻時間秒 = 秒(冷卻時間)
        if 冷卻時間秒 > 30:
            倒數時間 = 冷卻時間秒
            print('\r' + 到期時間 + ' 倒數中請稍後... ' + str(倒數時間) ,end="")
        time.sleep(0.01)