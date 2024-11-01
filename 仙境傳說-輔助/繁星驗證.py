from  win32com.client import Dispatch
import time,os,win32gui,re
from time import sleep
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
        # self.path = self.dm.GetBasePath()+Path
        # self.dm.SetPath(self.path)
        # print('\t附件路徑存放: ',self.path)
        # dm_ret = self.dm.SetDict(0, "驗證.txt")
        # print('\t字典返回:'+ str(dm_ret)) # dm_ret類型轉換str
        # dm_ret = self.dm.BindWindow(self.hwnd,'gdi','dx2','dx',4)
        # if dm_ret == 1:
        #     print('\t綁定成功')
        # else:
        #     print(' 綁定失敗')
    def ReadStr(self,read,數量):
        ReadStr = self.dm.ReadString(self.hwnd, read, 0, 數量)
        length = len(ReadStr)
        return ReadStr

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
    decimal_number = 24
    while(1):
        read = f'[[[[<Yuno.exe>+00E25D68]+94]+c0]+0]+0'
        input_str = job.ReadStr(read,500)
        #if input_str == '[^003366防外掛驗證^000000]':
        print(input_str)
        if input_str == '[^003366防外掛驗證^000000]':
            for i in range(1,6):
                hex_number = hex(decimal_number*i)[2:]
                read = f'[[[[<Yuno.exe>+00E25D68]+94]+c0]+{hex_number}]+0'
                input_str = job.ReadStr(read,50)
                if input_str:
                    print(input_str)
                    pattern = r'\^i\[(\d+)\]'
                    match = re.search(pattern, input_str)
                else:
                    match = ''
                if match:
                    result = match.group(1)
                    print(result)
        sleep(1)