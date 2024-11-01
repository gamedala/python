from  win32com.client import Dispatch
from  time import sleep
import win32gui
import time
import ctypes
dms = ctypes.windll.LoadLibrary('C:/dm/DmReg.dll')
Path = '亂2'

class Operation:
    def __init__(self):
        value = 0
        dms.SetDllPathW('C:/dm/dm7.dll', 0)
        try:
            self.dm = Dispatch('dm.dmsoft') #創建DM
            print("\t大漠插件版本: ",self.dm.Ver())
        except Exception:
            quit()
        self.hwnd = win32gui.FindWindow(None,"亂2 online") # 窗口標題
        self.path = self.dm.GetBasePath() + Path
        self.dm.SetPath(self.path)
        print(f'\t附件路徑存放: {self.path}')
        while value == 0:
            dm_ret = self.dm.SetDict(0, "字典.txt") #大漠字典設定
            value = self.dm.GetDictCount(0)
            time.sleep(0.1)
            if value > 0:
                print(f'\t字典返回: {str(dm_ret)} - {value}')
            else:
                self.dm.ClearDict(0)
        if not(self.hwnd) :
            print(' 未找到句柄')
            quit()
        self.Dm_Reg("jv965720b239b8396b1b7df8b768c919e86e10f","jfiax8yhxfpyqy7","121.204.252.143") # 註冊
        dm_ret = self.dm.SetWindowState(self.hwnd,12) # 恢復並激活指定窗口
        print(f'\t窗口大小: {self.dm.GetClientSize(self.hwnd)}')
        dm_ret = self.dm.BindWindowEx(self.hwnd,"gdi","dx.mouse.position.lock.api|dx.mouse.clip.lock.api|dx.mouse.input.lock.api|dx.mouse.state.api|dx.mouse.state.message|dx.mouse.api|dx.mouse.cursor","dx.keypad.input.lock.api|dx.keypad.state.api|dx.keypad.api","dx.public.active.api|dx.public.active.message|dx.public.focus.message",0)
        if dm_ret == 1:
            print('\t綁定成功')
        else:
            print(' 綁定失敗')
            quit()

    def Dm_Reg(self,註冊碼,附加,IP): # 註冊
        dm_ret = self.dm.RegEx(註冊碼,附加,IP)
        dm_res = {
			-1 : "可能防火牆攔截,如果可以正常訪問大漠插件網站，那就可以肯定是被防火牆攔截" ,
			-2 : "進程沒有以管理員方式運行" ,
			0 : "未知錯誤" ,
			1 : "\t成功註冊,使用腳本插件需要付費,依照使用時間計價,請勿給他人使用 ^_^y" ,
			2 : "餘額不足" ,
			3 : "綁定了本機器，但是賬戶餘額不足50元" ,
			4 : "註冊碼錯誤" ,
			5 : "你的機器或者IP在黑名單列表中或者不在白名單列表中" ,
			6 : "非法使用插件. 一般出現在定制插件時，使用了和綁定的用戶名不同的註冊碼" ,
			7 : "你的帳號因為非法使用被封禁" ,
			8 : "ver_info不在你設置的附加白名單中" ,
			77 : "機器碼或者IP因為非法使用，而被封禁" ,
			777 : "同一個機器碼註冊次數超過了服務器限制" ,
			-8 : "版本附加信息長度超過了20" ,
			-9 : "版本附加信息裡包含了非法字母" ,
			-10 : "非法的參數ip" 
        }
        print(f'大漠註冊狀態: {dm_res[dm_ret]}')

    def 按鍵(self,座標,顏色): # 按鍵
        color = self.dm.GetColor(座標[0],座標[1])
        if color == 顏色 :
            print(f"是{顏色}")

    def 按鍵(self,KEY_ID): # 按鍵
        self.dm.keydown(KEY_ID)
        self.dm.keyup(KEY_ID)

    def 移動點擊(self,x,y,delays): # 滑鼠移動點擊
        self.dm.MoveTo(x,y)
        time.sleep(delays/1000)
        self.dm.LeftClick()
    
    def 文字識別(self,名稱,位置,顏色,大小寫): # 文字識別
        dm_ret = self.dm.Ocr(位置[0],位置[1],位置[2],位置[3],顏色,1.0)
        if 大小寫 == 1 :
            dm_ret = dm_ret.upper() # 轉換大寫
        print(f'{名稱}: {dm_ret}')
        return dm_ret
    
    def 找字(self,位置,ocr,core,sin,偏移,delays):
        self.xy = self.dm.FindStr(位置[0],位置[1],位置[2],位置[3],ocr,core,sin)
        if self.xy[1] > 0:
            print("找到 [" + ocr + "] "+ " X: " + str(self.xy[1]) + " - Y: " + str(self.xy[2]) + " 偏移X: " + str(偏移[0]) + " - 偏移Y: " + str(偏移[1]) + " delay: " + str(delays))
            if delays > 0:
                time.sleep(0.5)
                self.dm.MoveTo(self.xy[1]+偏移[0],self.xy[2]+偏移[1])
                self.dm.LeftClick()
                time.sleep(delays/1000)
            return True
        else:
            return False
        
    def convert(self): # 識別轉轉樂安全碼 184,473,413,525
        self.文字識別('抽獎轉轉樂',[284,148,613,270],'f5f5f5-000000',0)
        if self.找字([284,148,613,270], "抽獎轉轉樂", "f5f5f5-000000", 1.0, (240,326), 250) == True:
            string = self.文字識別('轉轉樂安全碼',[440,254,766,312],'f01010-000000|10f0f0-000000|f0f010-000000|10f010-000000|f010f0-000000|f0f0f0-000000|f08010-000000',0)
            English = self.文字識別('參照安全碼英文',[417,366,783,403],'f01010-000000|10f0f0-000000|f0f010-000000|10f010-000000|f010f0-000000|f0f0f0-000000|f08010-000000',1)
            count = self.文字識別('參照安全碼數字',[417,406,782,440],'f01010-000000|10f0f0-000000|f0f010-000000|10f010-000000|f010f0-000000|f0f0f0-000000|f08010-000000',0)
            if string and English and count:
                self.string = string # 轉轉樂安全碼
                self.English = English # 參照英文
                self.count = count # 參照數字
                dictionary = dict(zip(self.English, self.count)) # 反回字典
                if dictionary:
                    char_list = list(self.string) # 拆開轉轉樂安全碼字串
                    for i in char_list: # 遍歷字符列表，搜尋每個字符對應數值
                        print("按鍵 '{}' 對應的數值: {}".format(i, self.search_value(dictionary, i)))
                    self.移動點擊(self.xy[1]+325,self.xy[2]+325,10)
                    sleep(0.5)
                    self.移動點擊(self.xy[1]+378,self.xy[2]+7,10)
        else:
            self.dm.Capture(284,148,613,270,"screen.bmp")
    
    def search_value(self, dictionary, key): # 字典匹配
        if key in dictionary:
            self.按鍵(96+int(dictionary[key]))
            sleep(0.5)
            return dictionary[key]
        else:
            return "不存在字典"

    def 驗證(self):
        顏色數量 = self.dm.GetColorNum(500,80,580,100,"000000-000000",1.0)
        # print(顏色數量)
        if 顏色數量 == 196:
            self.移動點擊(536,43,250)
            sleep(1)
            self.convert()

if __name__ == "__main__":
    job = Operation() # 註冊插件
    while 1:
        job.驗證()
        sleep(1)