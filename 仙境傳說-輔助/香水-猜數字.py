import itertools
import random
import re
from win32com.client import Dispatch
import ctypes, win32gui
from time import sleep,time
dm_path = r"C:\dm\dm.dll"
DmReg_path = r"C:/dm/DmReg.dll"
Path = '香水'
dms = ctypes.windll.LoadLibrary(DmReg_path)

# 生成所有可能的三位數字組合
def generate_all_possible():
    return [''.join(p) for p in itertools.permutations('123456789', 3)]

def get_feedback(guess, answer):
    A = sum(1 for g, a in zip(guess, answer) if g == a)
    B = sum(1 for g in guess if g in answer) - A
    return A, B

def filter_possible(possible_list, guess, A, B):
    return [p for p in possible_list if get_feedback(guess, p) == (A, B)]

def select_next_guess(possible_list, all_candidates):
    min_max = None
    best_guess = None

    for guess in all_candidates:
        feedback_counts = {}
        for answer in possible_list:
            feedback = get_feedback(guess, answer)
            feedback_counts[feedback] = feedback_counts.get(feedback, 0) + 1

        worst_case = max(feedback_counts.values())
        if min_max is None or worst_case < min_max:
            min_max = worst_case
            best_guess = guess
            
    return best_guess

class Operation:
    def __init__(self):
        value = 0
        dms.SetDllPathW(dm_path, 0)
        self.dm = Dispatch('dm.dmsoft')
        print("\t大漠插件版本: ",self.dm.Ver())
        self.hwnd = win32gui.FindWindow(None,"1234567890          ")
        self.path = self.dm.GetBasePath()+Path
        self.dm.SetPath(self.path)
        while value == 0:
            dm_ret = self.dm.SetDict(0, "字典.txt") #大漠字典設定
            value = self.dm.GetDictCount(0)
            sleep(0.1)
            if value > 0:
                print(f'\t字典返回: {str(dm_ret)} - {value}')
            else:
                self.dm.ClearDict(0)
        dm_ret = self.dm.BindWindow(self.hwnd,'gdi','dx2','dx',4)
        if dm_ret == 1:
            print('\t綁定成功')
        else:
            print(' 綁定失敗')
            quit()

    def 移動點擊(self, xy, delays):
        self.dm.MoveTo(xy[0], xy[1])
        self.dm.LeftClick()
        self.dm.MoveTo(0, 0)
        if delays > 0 :
            sleep(delays / 1000)

    def 按鍵(self,KEY_ID):
        self.dm.keydown(KEY_ID)
        self.dm.keyup(KEY_ID)

    def 按鍵2(self,KEY_ID):
        self.dm.KeyDownChar(KEY_ID)
        self.dm.KeyUpChar(KEY_ID)

    def 拆分輸入(self,number_string):
        for digit in number_string:
            #numbers.append(int(digit))
            self.按鍵(48+int(digit))
            #sleep(0.05)
        
    def 記憶體字串(self,位置,字串):
        return self.dm.ReadString(self.hwnd, 位置, 0, 字串)

    def 寫記憶體字串(self,位置,字串):
        self.dm.WriteString(self.hwnd, 位置,0 ,字串)

    def 記憶體數值(self,位置):
        return self.dm.ReadInt(self.hwnd, 位置, 0)
    
    def 寫記憶體數值(self,位置,數值):
        self.dm.WriteInt(self.hwnd,位置,0,數值)
        return
    
    def 窗口發送文本(self,文本):
        self.dm.SendString2(self.hwnd,文本)
        return
    
    def 找字(self,位置,文字,顏色,偏移,type):
        xy = self.dm.FindStrWithFont(位置[0],位置[1],位置[2],位置[3],文字,顏色, 1.0, "細明體", 9, 0)
        if xy[1] > -1 :
            if type == True:
                self.移動點擊([xy[1]+偏移[0],xy[2]+偏移[1]],0)
            else:
                return xy
            return True
        else:
            return False
    
    def 識別文字(self,位置,顏色):
        str = self.dm.Ocr(位置[0],位置[1],位置[2],位置[3],顏色,1.0)
        return str
    
if __name__ == '__main__':
    job = Operation() # 註冊插件
    初始化 = False
    猜數字總時間 = 錯誤 = 猜數字次數 = 次數 = 重置 = 0
    猜數字時間 = time()
    all_possible = []
    選單次數 = False
    aa = True
    while True: # 迴圈
        if aa == True:
            if job.記憶體數值("01173108") > 0: # 對話
                if job.記憶體數值("01173110") > 0 and 選單次數 == False: # 選單
                    選單次數 = True
                    job.寫記憶體數值("[[<香水仙境_2024-08-18.exe>+00D73110]+A4]+94",1)
                job.按鍵(13)
            else:
                選單次數 = False
                job.移動點擊([461,336],100)
                
        else:
            if job.記憶體數值("01173108") > 0: # 對話
                if 初始化 == False: # 初始化
                    初始化 = True
                    all_possible = generate_all_possible()
                    猜數字次數 = 0
                    猜數字時間 = time()
                    次數 += 1
                if job.記憶體數值("01173230") > 0: # 輸入框
                    A, B = "", ""
                    if len(all_possible) > 1: # 答案大於1
                        if 猜數字次數 == 0:
                            guess = random.choice(all_possible) # 隨機選擇一個初始猜測數字
                        else:
                            guess = select_next_guess(all_possible, all_possible)
                    elif len(all_possible) == 1: # 如果只剩下一個可能的選擇，直接猜測
                        guess = all_possible[0]
                    猜數字次數 += 1
                    job.寫記憶體字串("013EF0CC", f'{guess}') # 字符串
                    job.寫記憶體數值("013EF0DC", 3) # 長度
                    job.按鍵(13)
                    while A == "" and job.記憶體數值("01173108") > 0: # 迴圈尋找 A B
                        job.按鍵(13)
                        sleep(0.25)
                        if '猜出正確答案的時間是' == job.記憶體字串("[[[[<香水仙境_2024-08-18.exe>+00D73108]+94]+c0]+60]+0", 99): # 退出迴圈
                            job.按鍵(13)
                            break
                        elif job.記憶體數值("01173230") > 0: # 出現輸入框 放棄本輪
                            job.寫記憶體字串("013EF0CC", '123456') # 字符串
                            job.寫記憶體數值("013EF0DC", 6) # 長度
                            錯誤 += 1
                        else:
                            # 取得 A B 值
                            A_match = re.search(r"\^FF3152(\d)\^", job.記憶體字串("[[[[<香水仙境_2024-08-18.exe>+00D73108]+94]+c0]+30]+0", 99))
                            B_match = re.search(r"\^FF3152(\d)\^", job.記憶體字串("[[[[<香水仙境_2024-08-18.exe>+00D73108]+94]+c0]+48]+0", 99))
                            if A_match and B_match:
                                A = A_match.group(1)
                                B = B_match.group(1)
                                all_possible = filter_possible(all_possible, guess, int(A), int(B))
                else: # 無輸入框
                    if job.記憶體數值("01173110") > 0: # 選單
                        job.寫記憶體數值("[[<香水仙境_2024-08-18.exe>+00D73110]+A4]+94",2)
                job.按鍵(13)
                sleep(0.15)
            else: # 無對話
                job.找字([91,66,893,596],"猜數字遊戲","000000-000000",[35,40],True)
                初始化 = False
                if 猜數字時間 < time() :
                    花費 = time() - 猜數字時間
                    猜數字總時間 += 花費
                    if 次數 > 0 :
                        print(f'\r次數: {次數} 錯誤: {錯誤} 上次時間: {花費:.2f} 上次猜了: {猜數字次數} 總共時間: {猜數字總時間:.2f} 平均: {猜數字總時間/次數:.2f}',end="")
                sleep(0.2)
        sleep(0.05)