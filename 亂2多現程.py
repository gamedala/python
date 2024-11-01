import tkinter as tk
from tkinter import messagebox
import threading
import time
import requests
from  win32com.client import Dispatch
from  time import sleep
import win32gui
import ctypes
dms = ctypes.windll.LoadLibrary('C:/dm/DmReg.dll')
Path = "亂2"
api_url = "https://ap8.ragic.com/rank/forms2/1" # 網址 改為自己的網址
headers  = {
    "Authorization": "Basic Vk1UQTZrVnFaVlZGSXg4a2VRYkVXMjJ4SHkxOTYzUUzUmptLzBjTEFwU0hCTUR0VGlhb2V1VHJhblgyVldTOQ=="
} # 金鑰 Basic'空白'後面改自己金鑰
params ={
    'api': '',
    'v': 1
} # 不用動

# 多線程
class WorkerThread(threading.Thread):
    def __init__(self, task, *args):
        super().__init__()
        self.task = task
        self.args = args
        self._stop_event = threading.Event()

    def run(self):
        while not self._stop_event.is_set():
            self.task(*self.args)
        print(f'Thread {self.name} stopped.')

    def stop(self):
        self._stop_event.set()
# 主線
class MainThread:
    def __init__(self):
        self.threads = []

    def create_and_start_thread(self, task, *args):
        worker = WorkerThread(task, *args)
        self.threads.append(worker)
        worker.start()

    def stop_all_threads(self):
        for thread in self.threads:
            thread.stop()
        for thread in self.threads:
            thread.join()
        self.threads = []
# UI介面
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        master.geometry("450x150")
        self.pack()
        self.create_widgets()
        self.job_manager = MainThread()

    def create_widgets(self):
        self.start_button = tk.Button(self, text="Start", command=self.start_job)
        self.start_button.grid(row=0, column=0, padx=10, pady=10)

        self.stop_button = tk.Button(self, text="Stop", command=self.stop_job)
        self.stop_button.grid(row=0, column=1, padx=10, pady=10)

        self.quit_button = tk.Button(self, text="QUIT", fg="red", command=on_closing)
        self.quit_button.grid(row=0, column=2, padx=10, pady=10)

        self.status_label = tk.Label(self, text="Status: Ready")
        self.status_label.grid(row=1, column=0, columnspan=3, sticky="ew")

        self.text_to_copy = tk.StringVar()
        self.text_to_copy.set("")
        
        self.copy_text_label = tk.Entry(self, textvariable=self.text_to_copy, state='readonly', readonlybackground='white')
        self.copy_text_label.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
        self.copy_text_label.config(width=35)
        self.copy_text_label.bind("<Button-1>", self.copy_to_clipboard)

        self.大漠註冊()

    def 大漠註冊(self):
        value = 0
        dms.SetDllPathW('C:/dm/dm7.dll', 0)
        try:
            self.dm = Dispatch('dm.dmsoft') #創建DM
            print("\t大漠插件版本: ",self.dm.Ver())
        except Exception:
            quit()
        self.machine_code = self.dm.GetMachineCodeNoMac() # 獲取機碼
        self.text_to_copy.set(self.machine_code)
        if self.機碼序號檢查() : # 檢查機碼是否存在表單
            self.hwnd = win32gui.FindWindow(None,"亂2 online") # 窗口標題
            self.path = self.dm.GetBasePath() + Path
            self.dm.SetPath(self.path)
            print(f'\t附件路徑存放: {self.path}')
            while value == 0:
                dm_ret = self.dm.SetDict(0, "字典.txt") #大漠字典設定
                value = self.dm.GetDictCount(0)
                sleep(0.1)
                if value > 0:
                    print(f'\t字典返回: {str(dm_ret)} - {value}')
                else:
                    self.dm.ClearDict(0)
            if not(self.hwnd) :
                print(' 未找到句柄')
                quit()
            self.Dm_Reg("jv965720b239b8396b1b7df8b768c919e86e10f","ji3wtqx5t9a9wp7","121.204.252.143") # 註冊
            dm_ret = self.dm.SetWindowState(self.hwnd,12) # 恢復並激活指定窗口
            print(f'\t窗口大小: {self.dm.GetClientSize(self.hwnd)}')
            dm_ret = self.dm.BindWindowEx(self.hwnd,"gdi","dx.mouse.position.lock.api|dx.mouse.clip.lock.api|dx.mouse.input.lock.api|dx.mouse.state.api|dx.mouse.state.message|dx.mouse.api|dx.mouse.cursor","dx.keypad.input.lock.api|dx.keypad.state.api|dx.keypad.api","dx.public.active.api|dx.public.active.message|dx.public.focus.message",0)
            if dm_ret == 1:
                print('\t綁定成功')
            else:
                print(' 綁定失敗')
                quit()
            self.threads = []

    def 機碼序號檢查(self):
        response = requests.get(api_url, params=params,headers=headers)
        # 檢查狀態碼和輸出結果
        if response.status_code == 200:
            data = response.json()
            print(f'回傳信息: {data}')
            #serial_numbers = [entry['硬體序號'] for entry in data.values()]
            serial_numbers = [entry['硬體序號'] for entry in data.get('data', [])]
            if self.machine_code in serial_numbers:
                self.update_status(f"序號 {self.machine_code} 存在於列表中。")
                return 1
            else:
                self.master.clipboard_clear() 
                self.master.clipboard_append(self.text_to_copy.get()) # 貼上剪貼簿
                messagebox.askokcancel("提醒", f"序號不再信任名單, 請直接Ctrl+V訊息給作者。", icon=messagebox.INFO)
                return 0
        else:
            self.update_status('檢索資料失敗:', response.status_code, response.text)
            return 0

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

    def 按鍵(self,KEY_ID): # 按鍵
        self.dm.keydown(KEY_ID)
        self.dm.keyup(KEY_ID)

    def 移動點擊(self,x,y,delays): # 滑鼠移動點擊
        self.dm.MoveTo(x,y)
        sleep(delays/1000)
        self.dm.LeftClick()

    def 滑鼠移動(self,x,y):
         self.dm.MoveTo(x,y)
    
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
                sleep(0.5)
                self.dm.MoveTo(self.xy[1]+偏移[0],self.xy[2]+偏移[1])
                self.dm.LeftClick()
                sleep(delays/1000)
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
            self.歸位()
            self.移動點擊(536,43,250)
            sleep(1)
            self.convert()
            self.地圖()
            self.按鍵(73)
            sleep(0.5)

    def 仿真移動(self,起始,結束,duration=1.0): # 滑鼠長案移動
        self.dm.moveto(起始[0],起始[1])
        self.dm.RightDown()
        start_time = time.time()
        end_time = start_time + duration
        print(f"起始座標({起始[0]},{起始[1]})")

        while time.time() < end_time :
            elapsed_time = time.time() - start_time
            progress = elapsed_time / duration
            current_x = int(起始[0]+(結束[0]-起始[0])*progress)
            current_y = int(起始[1]+(結束[1]-起始[1])*progress)
            self.dm.moveto(current_x,current_y)
            time.sleep(0.1)
        print(f"達到座標({結束[0]},{結束[1]})")
        self.dm.RightUp()

    def 技能輸出(self):
                self.仿真移動([450,475],[800,250],0.15)
                self.仿真移動([800,250],[800,650],0.15)
                self.仿真移動([800,650],[1300,475],0.15)
                self.仿真移動([1300,475],[450,475],0.15)
                self.按鍵(112)
                print(f"完成技能")

    def 必殺(self): #必殺
            print(f"必殺")
            self.按鍵(115)
            sleep(0.8)
            color = self.dm.GetColor(10,415)
            if color == "db8400" :# 確認是否已使用
                print(f"使用必殺")
                sleep(0.1)
                self.按鍵(48)
                self.技能輸出() #修改
            else:
                self.按鍵(112)
                sleep(0.5)
                print(f"未完成技能")

    def 劍(self,x,座標,顏色):
            print(f"x")
            sleep(0.1)
            color = self.dm.GetColor(座標[0],座標[1])
            if color == 顏色 :# 確認是否已使用
                print(f"x")
                sleep(0.1)
                self.按鍵(48+x)
                self.技能輸出()
            else:
                print(f"未完成技能")

    def 空白(self):
        i = 0
        while (i<15):
            print(f"撿")
            self.按鍵(32)
            sleep(0.2)
            i += 1

    def 位移(self):
            print(f"位移")
            self.移動點擊(800,483,250)

    def 地圖(self):
            print(f"開啟地圖")
            self.按鍵(77)
            sleep(0.1)
            self.仿真移動([1388,160],[1369,97],0.2)
            sleep(0.1)
            self.仿真移動([1369,97],[1388,160],0.2)
            sleep(0.1)

    def 歸位(self):
        print(f"歸位")
        self.移動點擊(1431,150,0.1)
        self.移動點擊(1431,150,0.1)
        sleep(1.5)

    def 左偏(self):
        print(f"歸位")
        self.移動點擊(1361,150,0.1)
        self.移動點擊(1361,150,0.1)
        sleep(1.5)

    def 右偏(self):
        print(f"歸位")
        self.移動點擊(1478,150,0.1)
        self.移動點擊(1478,150,0.1)
        sleep(1.5)    

    def start_job(self):
        self.job_manager.create_and_start_thread(self.sample_task, 1)
        self.job_manager.create_and_start_thread(self.cc)

    def stop_job(self):
        self.job_manager.stop_all_threads()

    def sample_task(self, duration):
        print(f'任務運行時間為 {duration} 秒...')
        time.sleep(duration)
        print('任務完成.')

    def cc(self):
        self.update_status("cc 任务结束")
        self.地圖()
        while not threading.current_thread()._stop_event.is_set():
            self.歸位()
            self.必殺()
            a = 0
            while (a<1):
                if threading.current_thread()._stop_event.is_set():
                    break
                self.劍(1,[19,74],"4077f7")
                self.劍(2,[20,111],"638ead")
                self.劍(3,[16,151],"867ad9")
                self.劍(4,[20,188],"907053")
                self.劍(5,[18,226],"b04a25")
                self.劍(6,[14,264],"cb8042")
                self.劍(7,[21,302],"ffffff")
                self.劍(8,[22,339],"fffbef")
                self.劍(9,[19,378],"feffa8")
                self.劍(0,[17,416],"9f9fb5")
                self.空白()
                self.驗證()
                a += 1
                print(a)
            self.位移()
            sleep(1)
        
    def update_status(self, message): # 輸出文字
        self.status_label.config(text=f"狀態: {message}")
        self.status_label.update_idletasks()

    def copy_to_clipboard(self, event): # 複製剪貼簿
        self.master.clipboard_clear()
        self.master.clipboard_append(self.text_to_copy.get())
        self.update_status("文字已複製到剪貼簿")
    
    def on_quit(self):
        self.stop_job()
        self.master.destroy()

def on_closing():
    if messagebox.askokcancel("Quit", "你想退出嗎?"):
        app.on_quit()

root = tk.Tk()
root.title("多線程範例")
app = Application(master=root)
root.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()
