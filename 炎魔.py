import tkinter as tk
import threading
import time
from win32com.client import Dispatch
import os
import ctypes
import sys
import datetime
import json
from keyboard import add_hotkey

Path = '山櫻谷'  # 資料夾名稱
dms = ctypes.windll.LoadLibrary('C:/dm/DmReg.dll')

def is_admin():  # 檢查是否為系統管理員
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if is_admin():
        print("\t已獲取系統管理員權限")
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    return

class TimerApp:
    def __init__(self, master):
        dms.SetDllPathW('C:/dm/dm7.dll', 0)  # 設置DM.DLL路徑
        self.dm = Dispatch('dm.dmsoft')
        print("\t大漠插件版本: ", self.dm.Ver())
        self.hwnd = int(self.dm.EnumWindow(0, "旭日谷 #", "", 1 + 4 + 8 + 16))
        self.path = self.dm.GetBasePath() + Path  # 獲取路徑
        self.dm.SetPath(self.path)  # 設置路徑
        print('\t附件路徑存放: ', self.path)
        dm_ret = self.dm.SetDict(0, "字典.txt")  # 設置大漠字典
        print('\t字典返回:' + str(dm_ret))
        self.Dm_Reg("jv965720b239b8396b1b7df8b768c919e86e10f", "jzn0jzb3mpbx8f7", "121.204.252.143")  # 註冊
        dm_ret = self.dm.SetWindowState(self.hwnd,12) # 恢復並激活指定窗口
        dm_ret = self.dm.BindWindowEx(self.hwnd, "gdi", "dx.mouse.position.lock.api", "dx.keypad.input.lock.api|dx.keypad.state.api|dx.keypad.api", "", 11)
        if dm_ret == 1:
            print('\t綁定成功')
        else:
            print(' 綁定失敗')
            os._exit(0)

        self.master = master
        self.running = False
        self.seconds = 0
        self.scripttype = 0
        # 創建 UI 元件
        self.status_label = tk.Label(master, text="當前狀態: 未啟動", font=("標楷體", 14,"bold"))
        self.status_label.pack(pady=10)
        # 創建啟動/停止按鈕
        self.toggle_button = tk.Button(master, text="啟動(F5)", command=self.toggle_script, font=("細明體", 12))
        self.toggle_button.pack(pady=10)
        # 重新綁定
        self.resethwnd_button = tk.Button(master, text="重新綁定窗口", command=self.reset_hwnd, font=("細明體", 12))
        self.resethwnd_button.pack(pady=10)
        # 創建下拉選單
        self.create_dropdown_menu(master)
        # 設置窗口大小
        master.geometry("300x300")
        # 熱建檢查
        add_hotkey('F5', self.toggle_script)

    def Dm_Reg(self, 註冊碼, 附加, IP):  # 註冊
        try:
            dm_ret = self.dm.RegEx(註冊碼, 附加, IP)
            dm_res = {
                -1: "可能防火牆攔截,如果可以正常訪問大漠插件網站，那就可以肯定是被防火牆攔截",
                -2: "進程沒有以管理員方式運行",
                0: "未知錯誤",
                1: "\t成功註冊,使用腳本插件需要付費,依照使用時間計價,請勿給他人使用 ^_^y",
                2: "餘額不足",
                3: "綁定了本機器，但是賬戶餘額不足50元",
                4: "註冊碼錯誤",
                5: "你的機器或者IP在黑名單列表中或者不在白名單列表中",
                6: "非法使用插件. 一般出現在定制插件時，使用了和綁定的用戶名不同的註冊碼",
                7: "你的帳號因為非法使用被封禁",
                8: "ver_info不在你設置的附加白名單中",
                77: "機器碼或者IP因為非法使用，而被封禁",
                777: "同一個機器碼註冊次數超過了服務器限制",
                -8: "版本附加信息長度超過了20",
                -9: "版本附加信息裡包含了非法字母",
                -10: "非法的參數ip"
            }
            print(f'\t大漠註冊狀態: {dm_res[dm_ret]}')
        except Exception as e:
            print(f"註冊失敗: {e}")
        return

    def reset_hwnd(self): # 重新綁定窗口
        self.hwnd2 = int(self.dm.EnumWindow(0, "旭日谷 #", "", 1 + 4 + 8 + 16))
        if self.hwnd2 != self.hwnd or self.hwnd2 == 0 :
            dm_ret = self.dm.UnBindWindow()
            if dm_ret :
                print("解除綁定成功")
                self.hwnd = self.hwnd2
                dm_ret = self.dm.SetWindowState(self.hwnd,12) # 恢復並激活指定窗口
                dm_ret = self.dm.BindWindowEx(self.hwnd, "gdi", "dx.mouse.position.lock.api", "dx.keypad.input.lock.api|dx.keypad.state.api|dx.keypad.api", "", 11)
                if dm_ret == 1:
                    print('\t重新綁定成功')
                else:
                    print(' 重新綁定失敗')
            else:
                print("解除綁定失敗")
        else:
            print("窗口無須重新綁定")

    def create_dropdown_menu(self, master): # 下拉選單
        self.script_var = tk.StringVar(master)
        self.script_var.set("選擇腳本")
        self.script_menu = tk.OptionMenu(master, self.script_var, "A鍵打王", "X鍵打王", "掛機打怪", "SAO", "BS簡易", "BS普通","BS困難", "BS地獄","炎魔","暗黑龍王","皮卡啾", command=self.select_script)
        self.script_menu.config(font=("細明體", 12))
        self.script_menu.pack(pady=10)

    def select_script(self, selection): # 下拉選單執行腳本
        script_map = {
            "A鍵打王": 1,
            "X鍵打王": 2,
            "掛機打怪": 3,
            "SAO": 5,
            "BS簡易": 6,
            "BS普通": 7,
            "BS困難": 8,
            "BS地獄": 4,
            "炎魔"  : 9,
            "皮卡啾": 10,
            "暗黑龍王": 11
        }
        self.scripttype = script_map[selection] # 設定執行項目
        self.update_status(selection) # 輸出選擇項目
        self.update_menu_state()
        # script_map.get(selection, self.skill1_script)()

    def update_status(self, status_text):
        self.status_label.config(text=f"當前狀態: {status_text}")

    def update_menu_state(self):
        pass  # 下拉選單不需要禁用選項

    def toggle_script(self): # 腳本執行停止
        if not(self.scripttype) :
            print("未設定模式")
        elif self.running:
            self.cleanup()
            self.running = False
            self.update_status("已暫停")
            self.toggle_button.config(text="啟動(F5)")
            self.update_menu_state()
        else:
            self.running = True
            self.update_status("腳本運行中...")
            self.toggle_button.config(text="停止(F5)")
            self.timer_thread = threading.Thread(target=self.run_script)
            self.timer_thread.start()

    def 技能時間檢查(self):
        for 技能, (按鍵, 秒, 時間) in self.time_points.items():
            if time.time() > 時間:
                self.技能施放(技能, (按鍵, 秒, 時間))

    # 指定json讀取的部分
    def read_section(self,section_name):
        if section_name in self.data:
            return self.data[section_name]
        else:
            return 
    # 確保所有按鍵都被鬆開
    def cleanup(self):
        self.dm.KeyUp(88)  # X鍵
        print("X鍵已釋放")

    def 買幣(self):
        if self.找字(46,265,80,284, "2.0", "000000-000000|333333-000000|666666-000000|888888-000000", 0.8, (5,5), 50) == True :
            print (f'滿20E: {datetime.datetime.now().replace(microsecond=0)}')
            time.sleep(3)
            if self.找字2(8,50,44,86, "妙妙", "000000-000000", 0.8, (5,5), 1000) == True :
                print (f'點開商店: {datetime.datetime.now().replace(microsecond=0)}')
                time.sleep(1)
                self.dm.MoveTo(566,432)
                print (f'移動過去: {datetime.datetime.now().replace(microsecond=0)}')
                time.sleep(0.9)
                for _ in range (32) :
                    self.dm.WheelDown()
                    time.sleep(0.1)
                time.sleep(1)
                self.dm.MoveTo(470,441)
                print (f'移動到錢袋: {datetime.datetime.now().replace(microsecond=0)}')
                time.sleep(0.3)
                self.dm.LeftDoubleClick()
                time.sleep(0.3)
                self.dm.KeyPressStr(19,50)
                time.sleep(0.3)
                self.dm.MoveTo(728,419)
                print (f'我要確定囉: {datetime.datetime.now().replace(microsecond=0)}')
                time.sleep(0.3)
                self.dm.LeftClick()

    def 技能施放(self, 名稱, 時間):
        time.sleep(2)  # 等待2秒
        self.按鍵(時間[0], 500)  # 按按鍵，持續0.5秒
        self.time_points[名稱] = (時間[0], 時間[1], time.time() + int(時間[1]))  # 更新技能冷卻時間

    def 按鍵(self, 鍵碼, delays):
        self.dm.KeyDown(鍵碼)
        time.sleep(delays / 1000)
        self.dm.KeyUp(鍵碼)
    
    def 攻擊(self,鍵碼,delays):
        self.dm.KeyDown(鍵碼)
        time.sleep(delays/1000)
        self.dm.KeyUP(鍵碼)

    def 按鍵按down_up(self,鍵碼,delays):
        self.dm.KeyDown(鍵碼)
        time.sleep(delays/1000)
        self.dm.KeyUP(鍵碼)

    def 前上(self,鍵碼,鍵碼2):
        for i in range(2):
            self.dm.KeyDown(鍵碼)
            self.dm.KeyDown(鍵碼2)
            time.sleep(4)
            self.dm.KeyUP(鍵碼)
            self.dm.KeyUP(鍵碼2)
        self.dm.KeyUP(鍵碼2)
        time.sleep(0.5)

    def 找字(self, x1, y1, x2, y2, ocr, core, sin, 偏移, delays, type):
        xy = self.dm.FindStr(x1, y1, x2, y2, ocr, core, sin)
        if xy[1] > 0:
            if delays > 50:
                print("找到 [" + ocr + "] " + " X: " + str(xy[1]) + " - Y: " + str(xy[2]) + " 偏差X: " + str(偏移[0]) + " - 偏差Y: " + str(偏移[1]) + " delay: " + str(delays))
                time.sleep(0.25)
                self.dm.MoveTo(xy[1] + 偏移[0], xy[2] + 偏移[1])
                time.sleep(0.25)
                if type == 1:
                    for _ in range (2) :
                        self.dm.LeftDoubleClick()
                elif type == 2:
                    self.dm.LeftClick()
                self.dm.MoveTo(0,0)
                time.sleep(delays / 1000)
            return True
        else:
            return False
    
    def 找字2(self,x1,y1,x2,y2,ocr,core,sin,偏移,delays):
        xy = self.dm.FindStr(x1,y1,x2,y2,ocr,core,sin)
        if xy[1] > 0:
            if delays > 50:
                print("找到 [" + ocr + "] "+ " X: " + str(xy[1]) + " - Y: " + str(xy[2]) + " 偏差X: " + str(偏移[0]) + " - 偏差Y: " + str(偏移[1]) + " delay: " + str(delays))
                time.sleep(0.5)
                self.dm.MoveTo(xy[1]+偏移[0],xy[2]+偏移[1])
                time.sleep(0.25)
                for _ in range (2) :
                    self.dm.LeftDoubleClick()
                time.sleep(0.5)
                self.dm.MoveTo(0,0)
                time.sleep(delays/1000)     

    def 移動點擊(self, x, y, delays):
        self.dm.MoveTo(x, y)
        time.sleep(100 / 1000)
        self.dm.LeftClick()
        time.sleep(delays / 1000)

    def 持續攻擊(self):
        if time.time() < self.攻擊迴圈:
            if self.scripttype == 3:  # 掛機打怪
                #self.dm.KeyDown(65)  # A
                #self.dm.KeyUp(65)  # A
                self.技能時間檢查()  # 輔助技能
                if self.買幣1 < time.time():
                    self.買幣1 = time.time() + 60
                    self.買幣()
            if self.scripttype == 2:  # X鍵打王
                self.dm.KeyDown(88)  # X
            if self.scripttype == 1:  # A鍵打王
                self.dm.KeyDown(65)  # A
                self.dm.KeyUp(65)  # A
            if self.scripttype == 9:  # 炎魔
                self.dm.KeyDown(65)  # A
                self.dm.KeyUp(65)  # A
            if self.scripttype == 10:  #皮卡啾
                self.dm.KeyDown(65)  # A 
                self.dm.KeyUp(65)  # A
            if self.scripttype == 11:  #暗黑龍王
                self.dm.KeyDown(65)  # A 
                self.dm.KeyUp(65)  # A
            if self.scripttype == 4 or self.scripttype == 6 or \
                self.scripttype == 7 or self.scripttype == 8:  # BS地獄、簡易、普通、困難
                self.dm.KeyDown(65)  # A
                #self.dm.KeyUp(65)  # A
                self.技能時間檢查()  # 輔助技能
        else:
            self.dm.KeyUp(65)
            time.sleep(0.5)
            if self.左右走開關 == True:  # 左右走開關
                if self.左右 == False:
                    self.左右 = True
                    self.按鍵(37, 500)
                else:
                    self.左右 = False
                    self.按鍵(39, 500)
            self.攻擊迴圈 = time.time() + self.tacktime

    def run_script(self):
        # 自訂自動施放字典
        if not os.path.exists('time_points.json'):
            print("設定檔 time_points.json 不存在")
            self.update_status(f"time_points.json 不存在")
            self.running = False
        else:
            with open('time_points.json', 'r', encoding='utf-8') as file: # 讀取 json
                self.data = json.load(file)
            if self.scripttype == 3:
                self.time_points = self.read_section('AUTO') # 讀取指定設定
                print(f'AUTO設定讀取{self.time_points}')
            elif self.scripttype >= 4 and self.scripttype <= 9 :
                self.time_points = self.read_section('BSPQ') # 讀取指定設定
                print(f'BSPQ設定讀取{self.time_points}')
            self.tacktime = 1783  # 攻擊時間
            self.左右 = False
            self.左右走開關 = False
            self.攻擊迴圈 = time.time()
            self.買幣1 = time.time()
        while self.running:
            if self.scripttype == 11: #暗黑龍王                
                if self.找字(600,573,650,622, "暗|黑|龍|王", "ffff00-000000", 0.9, (10,-20), 350) == True :
                    print (f'龍: {datetime.datetime.now().replace(microsecond=0)}')
                    time.sleep(0.1)
                    self.按鍵按down_up(32,100)    
            if self.scripttype == 10: #皮卡啾
                if self.找字(712,573,798,622, "皮|卡|啾", "ffff00-000000", 0.9, (10,-20), 350) == True :
                    print (f'皮: {datetime.datetime.now().replace(microsecond=0)}')
                    time.sleep(0.1)
                    self.按鍵按down_up(32,100)
                    for i in range(4):
                        self.攻擊(39,500) # 前進
            if self.scripttype == 9: #炎魔
                if self.找字(449,573,504,613, "炎|魔", "ffff00-000000", 0.9, (10,-20), 350) == True :
                    print (f'炎魔: {datetime.datetime.now().replace(microsecond=0)}')
                    time.sleep(0.1)
                    self.按鍵按down_up(32,100)
                self.攻擊(39,200) # 前進
            if self.scripttype == 4 or ( self.scripttype >= 6 and self.scripttype <= 8 ): # BSPQ
                難度 = "","","","","地獄","","簡易","普通","困難"
                難度str = 難度[self.scripttype]
                if self.找字(831, 210, 1060, 396, "BSPQ", "ffff00-000000", 0.9, (10, -20), 150) == True:
                    print(f'我要開局BSPQ: {datetime.datetime.now().replace(microsecond=0)}')
                    self.update_status(f"我要開局BSPQ")
                if self.找字(577, 390, 917, 488, 難度str, "ffffff-000000", 0.8, (5, 5), 150) == True:
                    print(f'我要選{難度str}啦: {datetime.datetime.now().replace(microsecond=0)}')
                    self.update_status(f"我要選{難度str}")
            elif self.scripttype == 5: # SAO
                if self.找字(758,22,865,69, "AO|本", "ffff00-000000", 0.9, (10,-20), 800) == True :
                    print (f'我在一樓啦: {datetime.datetime.now().replace(microsecond=0)}')
                    self.update_status("我在一樓啦")
                    time.sleep(1)
                    self.按鍵按down_up(32,100)
                    time.sleep(2)
                    for i in range(4):
                        self.攻擊(39,1000) # 前進
                        self.攻擊(65,500) # 攻擊
                    self.前上(39,38) # 爬繩
                    time.sleep(0.3)
                    time.sleep(0.5)
                if self.找字(8,11,140,82, "2樓", "ffffff-000000", 0.9, (10,-20), 50) == True :
                    print (f'我在二樓啦: {datetime.datetime.now().replace(microsecond=0)}')
                    self.update_status("我在二樓啦")
                    for i in range(2):
                        self.攻擊(39,1000) # 前進
                        self.攻擊(65,500) # 攻擊
                    self.攻擊(39,5500) # 前進
                    time.sleep(0.3)
                time.sleep(0.5)
                if self.找字(8,11,140,82, "3樓", "ffffff-000000", 0.9, (10,-20), 50) == True :
                    print (f'我在三樓啦: {datetime.datetime.now().replace(microsecond=0)}')
                    self.update_status("我在三樓啦")
                    self.攻擊(39,1500) # 前進
                    self.攻擊(65,500) # 攻擊
                    time.sleep(0.3)
                    time.sleep(0.5)         
            if self.scripttype != 5:
                self.持續攻擊()
            time.sleep(0.1)
def main():
    run_as_admin()
    root = tk.Tk()
    root.title("Timer App")
    app = TimerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
